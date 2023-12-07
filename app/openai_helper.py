import openai


class OpenAiHelper:
    _key_path = '../openai_key'
    _message_log = []

    def __init__(self, message_log=None, model="gpt-3.5-turbo", temperature=0.1):
        openai.api_key = self._read_openai_key()

        if message_log:
            self._message_log = message_log
        self.model = model
        self.temperature = temperature

    def _read_openai_key(self):
        with open(self._key_path) as f:
            return f.readline()

    def send_user_message(self, message, model=None, temperature=None, functions=None):
        self._append_message_log(message, 'user')
        request = dict(
            model=self.model if model is None else model,
            messages=self._message_log,
            temperature=self.temperature,
        )

        if functions:
            request['functions'] = functions
            request['functions'] = 'auto'

        return openai.ChatCompletion.create(**request)

    def send_user_message_and_get_content(self, message):
        return self.send_user_message(message)['choices'][0]['message']['content']

    def _append_message_log(self, message, role):
        self._message_log.append({"role": role, "content": message})

