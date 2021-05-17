class User:
    def __init__(self, user_storage, username, chat_id):
        self._user_storage = user_storage
        self._username = username
        self._chat_id = chat_id

    @property
    def username(self):
        return self._username

    @property
    def chat_id(self):
        return self._chat_id

    @property
    def data(self):
        return self._user_storage._data[self._username].copy()

    def set_data(self, data_key, data):
        self._user_storage._data[self._username][data_key] = data
