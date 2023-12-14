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

class LangchainHelper:
    _openai_api_key = None
    _key_path = '../openai_key'
    _system_prompt = {}
    _history = []

    def __init__(self, model="gpt-3.5-turbo-16k", temperature=0.1, max_tokens=1024, max_history=10):
        self._openai_api_key = self._read_openai_key()
        self.chat = ChatOpenAI(
            openai_api_key=self._openai_api_key,
            model_name=model,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        self._max_history = max_history

    def _read_openai_key(self):
        with open(self._key_path) as f:
            return f.readline()

    def _append_to_history(self, message):
        self._history.append(message)
        if len(self._history) > self._max_history:
            self._history.pop(0)

    @property
    def system_prompt(self):
        return self._system_prompt

    @system_prompt.setter
    def system_prompt(self, prompt):
        self._system_prompt = SystemMessage(
            content=prompt,
        )

    def send_human_message(self, message: str):
        human_message = HumanMessage(content=message)

        self._append_to_history(human_message)
        request_prompts = [self._system_prompt] + self._history
        logging.info(f'request_prompts: {request_prompts}')
        ai_message = self.chat(request_prompts)
        logging.info(f'response: {ai_message}')
        self._append_to_history(ai_message)

        return ai_message