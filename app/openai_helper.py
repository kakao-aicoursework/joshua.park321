import logging

import openai


class OpenAiHelper:
    _key_path = '../openai_key'
    _system_prompt = {}
    _message_log = []

    def __init__(self, message_log=None, model="gpt-3.5-turbo-1106", temperature=0.1, max_tokens=1024):
        openai.api_key = self._read_openai_key()

        if message_log:
            self._message_log = message_log
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

    def _read_openai_key(self):
        with open(self._key_path) as f:
            return f.readline()

    def set_system_prompt(self, prompt):
        self._system_prompt = {
            'role': 'system',
            'content': prompt,
        }

    def send_user_message(self, message, model=None, temperature=None, functions=None, max_tokens=None):
        self._append_message_log(message, 'user')
        messages = [self._system_prompt] + self._message_log
        request = dict(
            model=self.model if model is None else model,
            messages=messages,
            temperature=self.temperature if temperature is None else temperature,
            max_tokens=self.max_tokens if max_tokens is None else max_tokens,
        )

        if functions:
            request['functions'] = functions
            request['functions'] = 'auto'

        response = openai.ChatCompletion.create(**request)
        logging.info(response)

        return response

    def send_user_message_and_get_content(self, message):
        return self.send_user_message(message)['choices'][0]['message']['content']

    def _append_message_log(self, message, role):
        self._message_log.append({"role": role, "content": message})

