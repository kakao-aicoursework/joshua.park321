

from project2.langchain_helper import LangchainHelper

def test_langchain_helper():
    langchain = LangchainHelper()
    langchain.system_prompt = '너는 그냥 챗봇이야 묻는말에 한국말로 답변하라'

    response = langchain.send_human_message('안녕 오늘 뭐먹지')

    print(response)

