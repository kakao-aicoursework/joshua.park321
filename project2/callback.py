from dto import ChatbotRequest
from samples import list_card
import requests
import time
import logging

from langchain_helper import LangchainHelper

SYSTEM_MSG = "당신은 카카오 서비스 제공자입니다."
logger = logging.getLogger("Callback")

langchain = LangchainHelper()
langchain.system_prompt = SYSTEM_MSG

def callback_handler(request: ChatbotRequest) -> dict:

    # # ===================== start =================================
    # response = openai.ChatCompletion.create(
    #     model="gpt-3.5-turbo",
    #     messages=[
    #         {"role": "system", "content": SYSTEM_MSG},
    #         {"role": "user", "content": request.userRequest.utterance},
    #     ],
    #     temperature=0,
    # )
    # # focus
    # output_text = response.choices[0].message.content

    logger.info(f"request: {request.userRequest.utterance}")
    ai_message = langchain.send_human_message(request.userRequest.utterance)
    output_text = ai_message.content

   # 참고링크 통해 payload 구조 확인 가능
    payload = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": output_text
                    }
                }
            ]
        }
    }
    # ===================== end =================================
    # 참고링크1 : https://kakaobusiness.gitbook.io/main/tool/chatbot/skill_guide/ai_chatbot_callback_guide
    # 참고링크1 : https://kakaobusiness.gitbook.io/main/tool/chatbot/skill_guide/answer_json_format

    time.sleep(1.0)

    url = request.userRequest.callbackUrl
    logger.info(f"callback url: {url}")

    if url:
        resp = requests.post(url=url, json=payload)
        logger.info(f"callback response: {resp.status_code}")
