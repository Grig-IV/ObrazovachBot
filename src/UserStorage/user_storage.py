from src.UserStorage.Models.user import User

class UserStorage:
    def __init__(self, allowed_usernames):
        self.allowed_usernames = allowed_usernames
        self.users = dict()

    def get_or_create_user(self, json_package):
        username = json_package.from_user.username
        user_id = json_package.from_user.id
        
        if username not in self.allowed_usernames:
            return None
        
        if not self.users.get(username):
            self.users[username] = User(username, user_id)
        
        return self.users[username]

    def get_users(self):
        return self.users.values()

    def get_users_db(self):
        users_db = dict()
        for username in self.users:
            users_db[username] = self.users[username].data

        return 'usersDate', users_db




    