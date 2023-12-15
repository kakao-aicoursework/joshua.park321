from project3.init_keys import init_keys


def pytest_configure(config):
    init_keys()
