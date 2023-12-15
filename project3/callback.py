from dto import ChatbotRequest
import requests
import time
import logging

from langchain_helper import LangchainHelper
from assets import data_카카오싱크

SYSTEM_MSG = f'''
당신은 카카오 서비스 제공자입니다. 제공되는 데이터를 참조해서 답변을 해주세요.
답변은 자세한 답변을 요구하기 전까지는 두세 문장의 짧은 답변을 하라
번호나 리스트 형태로 정리해서 답변하라

아래 데이터 중에, link 가 있다면 적극 사용하라.
데이터에 link 가 없다면 link 를 생성하려고 하지 마라

=============
{data_카카오싱크()}
'''

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
    user_id = request.userRequest.user.id

    logger.info(f"request: {request.userRequest.utterance}")
    ai_message = langchain.send_human_message(user_id, request.userRequest.utterance)
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
