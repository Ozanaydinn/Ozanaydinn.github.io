import requests
import os
from celery import Celery

celery = Celery(__name__)
    
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND")

@celery.task(name="analyze_hand", soft_time_limit=20)
def analyze_hand(image_data, session_id, user_id):
    resp = requests.post("http://34.118.87.165:5000/hand", {"data": image_data}).json()


    return {
            "hand_result": resp["hand_result"][0]["recognizedHandGesture"], 
            "session_id": session_id,
            "user_id": user_id
            }


@celery.task(name="analyze_head", soft_time_limit=30)
def analyze_head(image_data, session_id, user_id, timestamp):
    resp = requests.post("http://34.118.32.242:5000/head", {"data": image_data}).json()

    return {
            "head_pose_result": resp["head_pose_result"],
            "session_id": session_id,
            "user_id": user_id,
            "timestamp": timestamp
            }
