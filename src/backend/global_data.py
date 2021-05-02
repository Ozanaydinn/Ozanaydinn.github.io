from flask_sqlalchemy import SQLAlchemy
from models.StatisticsData import StatisticsData
import redis
import json
import os
from google.cloud import storage

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "hereapp-311315-96ceff393384.json"

REDIS_IP = os.environ.get("REDIS_IP")

r_envoy = redis.Redis(host=REDIS_IP, port=6379, db=0)
db = SQLAlchemy()
statistics = StatisticsData({})

bucket_name = "hereapp-files"

storage_client = storage.Client()
bucket = storage_client.bucket(bucket_name)

def init_cache():
    r_envoy.flushall()
    if not r_envoy.exists("statistics"):
        r_envoy.set("statistics", json.dumps(statistics.data))


