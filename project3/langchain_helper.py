import logging
import os
from typing import Union

from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import (
    SystemMessage, HumanMessage, AIMessage
)

from project3.chat_history import ChatHistoryHelper

class LangchainHelper:
    _openai_api_key = None
    _system_prompt = {}
    _history_helper = None

    def __init__(self, model="gpt-3.5-turbo-16k", temperature=0.1, max_tokens=1024, history_helper: ChatHistoryHelper=None):
        self.chat = ChatOpenAI(
            model_name=model,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        if history_helper:
            self._history_helper = history_helper

    def _append_to_history(self, user_id, message):
        if not self._history_helper:
            return
        self._history_helper.write_history(user_id, message)

    @property
    def system_prompt(self):
        return self._system_prompt

    @system_prompt.setter
    def system_prompt(self, prompt):
        self._system_prompt = SystemMessage(
            content=prompt,
        )

    def send_human_message(self, user_id, message: str):
        human_message = HumanMessage(content=message)
        request_prompts = self._get_request_prompts_with_history(user_id, human_message)
        logging.info(f'request_prompts: {request_prompts}')
        ai_message = self.chat(request_prompts)
        logging.info(f'response: {ai_message}')

        self._append_to_history(user_id, human_message)
        self._append_to_history(user_id, ai_message)

        return ai_message

    def _get_request_prompts_with_history(self, user_id, human_message):
        request_prompts = [self.system_prompt]
        if self._history_helper:
            request_prompts += self._history_helper.get_memory(user_id).buffer_as_messages
        request_prompts.append(human_message)
        return request_prompts

    def create_chain(self, prompt=None, template_file_path=None, output_key=None):
        _prompt = None
        if prompt:
            _prompt = prompt
        if template_file_path:
            _prompt = ChatPromptTemplate.from_template(template=open(template_file_path).read())
        if not _prompt:
            raise ValueError('prompt or prompt_file_path should be given')
        kwargs = dict(
            llm=self.chat,
            prompt=_prompt
        )
        if output_key:
            kwargs['output_key'] = output_key
        return LLMChain(**kwargs)
