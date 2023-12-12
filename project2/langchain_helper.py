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
    _key_path = '../openai_key'
    _system_prompt = {}
    _history = []

    def __init__(self, model="gpt-3.5-turbo-16k", temperature=0.1, max_tokens=1024):
        self.chat = ChatOpenAI(
            openai_api_key=self._read_openai_key(),
            model_name=model,
            temperature=temperature,
            max_tokens=max_tokens,
        )

    def _read_openai_key(self):
        with open(self._key_path) as f:
            return f.readline()

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

        self._history.append(human_message)
        request_prompts = [self._system_prompt] + self._history
        response = self.chat(request_prompts)

        return response