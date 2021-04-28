import requests
import os
from celery import Celery

celery = Celery(__name__)
    
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://10.220.160.203:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://10.220.160.203:6379")

@celery.task(name="analyze_hand", soft_time_limit=20)
def analyze_hand(image_data):
    return requests.post("http://34.118.87.165:5000/hand", {"data": image_data}).json()

@celery.task(name="analyze_head", soft_time_limit=30)
def analyze_head(image_data):
    return requests.post("http://34.118.79.23:5000/head", {"data": image_data}).json()