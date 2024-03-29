from models.User import User

class StatisticsData():

    def __init__(self, data):
        self.data = data
        
    '''
    {
        "24": {
            "user_id1": User()
            "user_id2": User()
        }
        ""
    }
    '''

    def add_session(self, session_id):
        if session_id not in self.data:
            self.data[session_id] = {}

            print("DATA: " , self.data)

            for key in self.data.keys():
                print("key value ", key)
                print("key type " , type(key))
            return "SUCCESS: Session successfully added!"

        return "ERROR: Session already added!"
    
    def add_user_to_session(self, session_id, email):

        if session_id in self.data:
            if email not in self.data[session_id]:
                self.data[session_id][email] = User().__dict__
                return "SUCCESS: User successfully added!"

            return "ERROR: User already added to the session!"

        return "ERROR: No such session!"

    def remove_session(self, session_id):

        if session_id in self.data:
            self.data.pop(session_id)

            return "SUCCESS: Session succesfully removed!"

        return "ERROR: No such session found!"

    def remove_user_from_session(self, session_id, email):

        if session_id in self.data:

            if email in self.data[session_id]:

                self.data[session_id].pop(email)

                return "SUCCESS: User succesfully removed from session!"

            return "ERROR: User was not found in the given session!"

        return "ERROR: Session not found!"






        