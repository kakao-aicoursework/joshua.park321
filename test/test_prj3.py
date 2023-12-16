from pprint import pprint

from project3.assets import AssetHelper
from project3.google_search import GoogleSearchHelper
from project3.langchain_helper import LangchainHelper


def test_prj3_main(tmp_path):
    user_message = '안녕 카카오소셜 어떻게 쓰는거야'
    template_path_base = '../project3/prompt_templates'

    langchain = LangchainHelper()
    asset_helper = AssetHelper(path_db=tmp_path)
    asset_helper.load()
    google_search_helper = GoogleSearchHelper()
    langchain.system_prompt = open(template_path_base + '/system.txt').read()

    chain_select_topic = langchain.create_chain(template_file_path=template_path_base + '/select_topic.txt', output_key='topic')
    chain_search_query = langchain.create_chain(template_file_path=template_path_base + '/generate_search_query.txt', output_key='search_query')
    chain_describe_topic = langchain.create_chain(
        template_file_path=template_path_base + '/describe_topic.txt',
        output_key='answer'
    )

    context = dict(
        topic_list=['카카오소셜', '카카오싱크', '카카오톡채널'],
        user_message=user_message,
    )

    context['topic'] = chain_select_topic.run(context)
    context['search_query'] = chain_search_query.run(context)
    context['web_search_result'] = google_search_helper.search(context['search_query'])
    context['document'] = asset_helper.query(context['search_query'])
    context['answer'] = chain_describe_topic.run(context)

    pprint(context)
    print(context['answer'])

