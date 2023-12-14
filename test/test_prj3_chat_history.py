from langchain_core.messages import HumanMessage

from project3.chat_history import ChatHistoryHelper


def test_chat_history(tmp_path):
    chat_history = ChatHistoryHelper(path_history=tmp_path)
    chat_history.write_history('user1', HumanMessage(content='message1'))
    chat_history.write_history('user1', HumanMessage(content='message2'))
    print(chat_history.get_memory('user1'))
