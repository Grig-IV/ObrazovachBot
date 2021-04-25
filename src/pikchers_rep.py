from src.models.pikcher import Pikcher

class PikchersRep:
    def __init__(self, pikchers_names):
        self.pikchers_names = pikchers_names
        self.pikchers = dict()

    def get_or_create_pikcher(self, username):
        username = json_package.from_user.username
        user_id = json_package.from_user.id
        
        if username not in self.pikchers_names:
            return None
        
        if not self.pikchers.get(username):
            self.pikchers[username] = Pikcher(username, user_id)
        
        return self.pikchers[username]



    