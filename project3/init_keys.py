import os


def openai_key():
    with open('../openai_key') as f:
        return f.readline()


def google_search_key():
    with open('../google_search_key') as f:
        api_key = f.readline()
        cse_id = f.readline()
        return api_key, cse_id


def init_keys():
    os.environ['OPENAI_API_KEY'] = openai_key()
    os.environ['GOOGLE_API_KEY'], os.environ['GOOGLE_CSE_ID'] = google_search_key()