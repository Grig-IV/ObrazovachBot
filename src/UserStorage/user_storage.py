import json

from src.UserStorage.Models.user import User


class UserStorage:
    def __init__(self, init_data_file_name):
        self._users = dict()
        self._init_data_file_name = init_data_file_name

        init_file = open(init_data_file_name, 'r')
        init_data = json.load(init_file)
        allowed_usernames = init_data["userData"].keys()
        self._data = {username: dict() for username in allowed_usernames}
        init_file.close()

    def get_users(self, key_func=None):
        if key_func is None:
            return self._users.values()

        users = list(filter(key_func, self._users.values()))
        return users

    def get_or_create_user(self, json_package):
        username = json_package.from_user.username
        user_id = json_package.from_user.id

        if username not in self._data.keys():
            return None

        if self._users.get(username):
            return self._users[username]

        init_file = open(self._init_data_file_name, 'r')
        init_data = json.load(init_file)
        user_data = init_data["userData"][username]
        default_user_data = init_data["defaultUserData"]

        user = User(self, username, user_id)
        for att in user_data:
            setattr(user, att, user_data[att])
        self._users[username] = user
        self._data[username] = default_user_data

        init_file.close()

        return user

    def get_users_db(self):
        return 'usersDate', self._data

    def set_users_db(self, db_dict):
        self._data = db_dict['usersDate']
