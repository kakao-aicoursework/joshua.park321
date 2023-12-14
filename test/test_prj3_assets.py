from project3.assets import AssetHelper
from project3.langchain_helper import LangchainHelper


def test_asset_helper(tmp_path):
    langchain = LangchainHelper()
    asset_helper = AssetHelper(langchain, path_db=str(tmp_path))
    asset_helper.load()

    result = asset_helper.query('카카오채널 어떻게 만드나')
    print(result)



