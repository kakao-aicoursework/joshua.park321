from project1.openai_helper import OpenAiHelper
from project1.assets import data_카카오톡채널


def test_openai_helper_with_asset():
    openai_helper = OpenAiHelper(max_tokens=4096)
    data = data_카카오톡채널()
    openai_helper.set_system_prompt(f'''
    너는 카카오톡 채널 문서를 읽고 유저의 질문에 답변하는 챗봇이다
    성실하게 데이터를 검토하고 적절한 답변을 해야 한다
    답변은 자세한 답변을 요구하기 전까지는 두세 문장의 짧은 답변을 하라
    
    참조할 데이터는 아래와 같다
    ===================
    {data}
    ''')

    resp = openai_helper.send_user_message_and_get_content('안녕 카카오톡 채널 어떻게 쓰는거야')
    print(resp)

    assert resp is not None


