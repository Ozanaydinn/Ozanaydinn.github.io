from models.User import User
from global_data import r_envoy
import json

class AnalyticsController:    

    def analyze_hand_result(data):
        hand_result = data["hand_result"]   
        session_id = data["session_id"]
        email = data["email"]

        positive_feedback_message = ""
        hand_raised = False

        if hand_result == 1 or hand_result == 5:
            with r_envoy.lock('my_lock'):

                stat = json.loads(r_envoy.get("statistics"))

                stat[session_id][email]["hand_results"].append(True)
                hand_raised = True

                r_envoy.set("statistics", json.dumps(stat))

                if len(stat[session_id][email]["hand_results"]) % 3 == 0:
                    positive_feedback_message = "You are actively participating to the lecture, keep going!"
                

        

        return {"feedback_message": positive_feedback_message, "hand_raised": hand_raised}

    def analyze_head_result(data):
        head_pose_result = data["head_pose_result"]   
        session_id = data["session_id"]
        email = data["email"]
        timestamp = data["timestamp"]

        pose_data = {
            "distracted": False,
            "timestamp": timestamp
        }

        feedback_message = ""

        if head_pose_result["horizontal"] != "straight":
            pose_data["distracted"] = True

        with r_envoy.lock('my_lock'):

            stat = json.loads(r_envoy.get("statistics"))

            user = stat[session_id][email]

            user["head_poses"].append(pose_data)

            if len(user["head_poses"]) == user["head_threshold"]: #If head poses reached threshold
                distracted_count = 0
                
                for pose in user["head_poses"]:

                    if pose["distracted"]:
                        distracted_count += 1

                if (user["head_threshold"] / 2) <= distracted_count:

                    time = user["head_poses"][-1]["timestamp"]
                    
                    user["head_distracted"].append(time)

                    #EMIT HEAD POSE DISTRACTED MESSAGE TO FRONT END
                    feedback_message = "You seem to be distracted, is everything okay?"

                user["head_poses"] = []

            r_envoy.set("statistics", json.dumps(stat))
        
        return {"feedback_message": feedback_message, "distraction_type": "head_pose"}

    def analyze_object(data):
        object_result = data["object_result"]   
        session_id = data["session_id"]
        email = data["email"]
        timestamp = data["timestamp"]

        phone_data = {
            "phone": False,
            "timestamp": timestamp
        }

        person_data = {
            "away": False,
            "timestamp": timestamp
        }

        if object_result["phone"]:
            phone_data["phone"] = True
    
        if object_result["person"] == 0:
            person_data["away"] = True

        feedback_message = ""

        with r_envoy.lock('my_lock'):
            stat = json.loads(r_envoy.get("statistics"))

            user = stat[session_id][email]

            user["phone_result"].append(phone_data)
            user["person_result"].append(person_data)

            if len(user["phone_result"]) == user["phone_threshold"]: #If phone reached threshold
                distracted_count = 0
            
                for result in user["phone_result"]:

                    if result["phone"]:
                        distracted_count += 1

                if (float(user["phone_threshold"]) / 2) <= distracted_count:

                    time = user["phone_result"][-1]["timestamp"]
                
                    user["phone_distracted"].append(time)

                    feedback_message = "Looking at your phone often can distract you." 

                user["phone_result"] = []

            if len(user["person_result"]) == user["person_threshold"]: #If phone reached threshold
                away_count = 0
            
                for result in user["person_result"]:

                    if result["away"]:
                        away_count += 1

                if away_count == user["person_threshold"]:

                    time = user["person_result"][-1]["timestamp"]
                
                    user["person_away"].append(time)

                    feedback_message = "Are you there?" 

                user["person_result"] = []
            
            r_envoy.set("statistics", json.dumps(stat))

        return {"feedback_message": feedback_message, "distraction_type": "object"}