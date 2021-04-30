from flask_sqlalchemy import SQLAlchemy
from models.StatisticsData import StatisticsData
import redis
import json
import os

REDIS_IP = os.environ.get("REDIS_IP")

r_envoy = redis.Redis(host=REDIS_IP, port=6379, db=0)

r_envoy.flushdb()

db = SQLAlchemy()
statistics = StatisticsData({})

if not r_envoy.exists("statistics"):
    r_envoy.set("statistics", json.dumps(statistics.data))

