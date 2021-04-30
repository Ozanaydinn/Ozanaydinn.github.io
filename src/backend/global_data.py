from flask_sqlalchemy import SQLAlchemy
from models.StatisticsData import StatisticsData
import redis
import json
import os

REDIS_IP = os.environ.get("REDIS_IP")

r_envoy = redis.Redis(host=REDIS_IP, port=6379, db=0)
db = SQLAlchemy()
statistics = StatisticsData({})

def init_cache():
    r_envoy.flushall()
    if not r_envoy.exists("statistics"):
        r_envoy.set("statistics", json.dumps(statistics.data))


