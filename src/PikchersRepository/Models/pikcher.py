class Pikcher:
    def __init__(self, pikcher_username, pikcher_id):
        self._username = pikcher_username
        self._id = pikcher_id

    @property
    def username(self):
        return self._username

    @property
    def chat_id(self):
        return self._id
