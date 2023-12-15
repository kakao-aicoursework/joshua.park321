from langchain.utilities import GoogleSearchAPIWrapper


class GoogleSearchHelper:

    def __init__(self):
        self._search = GoogleSearchAPIWrapper()

    def search(self, query, k=5):
        return self._search.results(query, k)
