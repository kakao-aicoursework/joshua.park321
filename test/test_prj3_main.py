from project3.main_bot import init_bot, main_bot_loop


def test_prj3_main(tmp_path):
    template_path_base = '../project3/prompt_templates'
    user_message = '안녕 카카오소셜 어떻게 쓰는거야'

    langchain, asset_helper, google_search_helper = init_bot(template_path_base=template_path_base, path_db=tmp_path)
    asset_helper.load()
    answer = main_bot_loop(user_message, langchain, asset_helper, google_search_helper, template_path_base=template_path_base)

    print(answer)
