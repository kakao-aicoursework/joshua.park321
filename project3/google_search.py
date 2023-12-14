from langchain.utilities import GoogleSearchAPIWrapper


class GoogleSearchHelper:
    _key_path = '../google_search_key'

    def __init__(self):
        self._read_google_search_key()
        self._search = GoogleSearchAPIWrapper(
            google_api_key=self._api_key,
            google_cse_id=self._cse_id,
        )

    def _read_google_search_key(self):
        with open(self._key_path) as f:
            self._api_key = f.readline()
            self._cse_id = f.readline()

    def search(self, query, k=5):
        return self._search.results(query, k)
