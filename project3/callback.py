from project3.dto import ChatbotRequest
import requests
import time
import logging

from project3.init_keys import init_keys
from project3.main_bot import init_bot, main_bot_loop

logger = logging.getLogger("Callback")

template_path_base = './project3/prompt_templates'
init_keys(base_dir='./')
langchain, asset_helper, google_search_helper = init_bot(template_path_base=template_path_base)
asset_helper.load()


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
    user_message = request.userRequest.utterance

    logger.info(f"request: {user_message}")
    output_text = main_bot_loop(user_message, langchain, asset_helper, google_search_helper, template_path_base=template_path_base)

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
