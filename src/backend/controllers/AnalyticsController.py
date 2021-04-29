from models.user import User
from global_data import statistics

class AnalyticsController:    

    def analyze_hand_result(data):
        hand_result = data["hand_result"]   
        session_id = data["session_id"]
        user_id = data["user_id"]

        positive_feedback_message = ""
        hand_raised = False
        
        print("DATA: " , statistics.data)

        for key in statistics.data.keys():
            print("key value ", key)
            print("key type " , type(key))


        if hand_result == 1 or hand_result == 5:
            user = statistics.data[session_id][user_id]
            user.hand_results.append(True)
            hand_raised = True
            
            if len(user.hand_results) % 3 == 0:
                positive_feedback_message = "You are actively participating to the lecture, keep going!"
        

        return {"feedback_message": positive_feedback_message, "hand_raised": hand_raised}

    def analyze_head_result(data):
        head_pose_result = data["head_pose_result"]   
        session_id = data["session_id"]
        user_id = data["user_id"]
        timestamp = data["timestamp"]

        pose_data = {
            "distracted": False,
            "timestamp": timestamp
        }

        feedback_message = ""

        if head_pose_result["horizontal"] != "straight":
            pose_data["distracted"] = True

        user = statistics.data[session_id][user_id]

        user.head_poses.append(pose_data)

        if len(user.head_poses) == user.head_threshold: #If head poses reached threshold
            distracted_count = 0
            
            for pose in user.head_poses:

                if pose["distracted"]:
                    distracted_count += 1

            if (user.head_threshold / 2) <= distracted_count:

                time = user.head_poses[-1]["timestamp"]
                
                user.head_distracted.append(time)

                #EMIT HEAD POSE DISTRACTED MESSAGE TO FRONT END
                feedback_message = "You seem to be distracted, is everything okay?"

            user.head_poses = []
        
        return {"feedback_message": feedback_message, "distraction_type": "head_pose"}

    def analyze_phone(data):
        phone_result = data["phone_result"]   
        session_id = data["session_id"]
        user_id = data["user_id"]
        stastics = data["statistics"]
        timestamp = data["timestamp"]

        phone_data = {
            "distracted": False,
            "timestamp": timestamp
        }

        user.phone_result.append(phone_data)

        feedback_message = ""

        if len(user.phone_result) == user.phone_threshold: #If phone reached threshold
            distracted_count = 0
            
            for result in user.phone_result:

                if result["distracted"]:
                    distracted_count += 1

            if (float(user.phone_threshold) / 2) <= distracted_count:

                time = user.phone_result[-1]["timestamp"]
                
                user.phone_distracted.append(time)

                #EMIT PHONE DISTRACTED MESSAGE TO FRONT END
                feedback_message = "Looking at your phone often can distract you." 

            user.phone_result = []

        return {"feedback_message": feedback_message, "distraction_type": "phone"}