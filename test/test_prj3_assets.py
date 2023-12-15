from project3.assets import AssetHelper


def test_asset_helper(tmp_path):
    asset_helper = AssetHelper(path_db=str(tmp_path))
    asset_helper.load()

    result = asset_helper.query('카카오채널 어떻게 만드나')
    print(result)



