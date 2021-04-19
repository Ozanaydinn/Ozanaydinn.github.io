from user import User

class Session:
    def __init__(self, uid_list): 
        self.students = []
        self.create_users(uid_list)

    def create_users(self,uid_list):
        for uid in uid_list:
            self.students.append(User(uid))
