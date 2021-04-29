from flask_sqlalchemy import SQLAlchemy
from models.statistics_data import StatisticsData

db = SQLAlchemy()
statistics = StatisticsData()