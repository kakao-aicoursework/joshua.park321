from project3.chat_history import ChatHistoryHelper
from project3.langchain_helper import LangchainHelper


def test_langchain_helper():
    langchain = LangchainHelper()
    langchain.system_prompt = '너는 그냥 챗봇이야 묻는말에 한국말로 답변하라'
    user_id = 'tester'

    response = langchain.send_human_message(user_id, '안녕 오늘 뭐먹지')
    print(response)
    response2 = langchain.send_human_message(user_id, '다른거 추천')
    print(response2)


def test_langchain_helper_with_history(tmp_path):
    chat_history_helper = ChatHistoryHelper(tmp_path)
    langchain = LangchainHelper(history_helper=chat_history_helper)
    langchain.system_prompt = '너는 그냥 챗봇이야 묻는말에 한국말로 답변하라'
    user_id = 'tester'

    response = langchain.send_human_message(user_id, '안녕 오늘 뭐먹지')
    print(response)
    response2 = langchain.send_human_message(user_id, '다른거 추천')
    print(response2)
