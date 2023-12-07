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

    @property
    def message_log(self):
        message_log = []
        if self._system_prompt:
            message_log.append(self._system_prompt)
        message_log.extend(self._message_log)
        return message_log

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
        request = dict(
            model=self.model if model is None else model,
            messages=self.message_log,
            temperature=self.temperature if temperature is None else temperature,
            max_tokens=self.max_tokens if max_tokens is None else max_tokens,
        )

        if functions:
            request['functions'] = functions
            request['functions'] = 'auto'

        response = openai.ChatCompletion.create(**request)
        logging.info(response)
        assistant_reply = self._extract_content_from_response(response)
        self._append_message_log(assistant_reply, 'assistant')

        return response

    def send_user_message_and_get_content(self, message):
        return self._extract_content_from_response(self.send_user_message(message))

    def _append_message_log(self, message, role):
        # TODO: max token 에 따라서 앞쪽 대화를 날려야 할수 있겠다
        self._message_log.append({"role": role, "content": message})

    @staticmethod
    def _extract_content_from_response(response):
        return response['choices'][0]['message']['content']
