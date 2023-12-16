import os


def openai_key(base_dir='../'):
    with open(base_dir + 'openai_key') as f:
        return f.readline()


def google_search_key(base_dir='../'):
    with open(base_dir + 'google_search_key') as f:
        api_key = f.readline()
        cse_id = f.readline()
        return api_key, cse_id


def init_keys(base_dir='../'):
    os.environ['OPENAI_API_KEY'] = openai_key(base_dir)
    os.environ['GOOGLE_API_KEY'], os.environ['GOOGLE_CSE_ID'] = google_search_key(base_dir)