class User:
    def __init__(self, username, user_id):
        self._username = username
        self._id = user_id
        self._date = dict()

    @property
    def username(self):
        return self._username

    @property
    def chat_id(self):
        return self._id

    @property
    def data(self):
        return self._date.copy()

    def set_data(self, data_key, data):
        self._date[data_key] = data