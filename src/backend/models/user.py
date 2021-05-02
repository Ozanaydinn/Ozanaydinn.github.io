class User: 
    def __init__(self): 
        self.hand_results = []
        self.head_poses = []
        self.phone_result = []
        self.person_result = []

        self.head_distracted = []
        self.phone_distracted = []
        self.person_away = []

        self.head_threshold = 6
        self.phone_threshold = 1
        self.person_threshold = 2