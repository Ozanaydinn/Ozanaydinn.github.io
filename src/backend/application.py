from flask import Flask, jsonify
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS

import controllers.AuthController as AuthController
import controllers.CourseController as CourseController
import controllers.FileController as FileController
import controllers.ImageController as ImageController
import controllers.SessionController as SessionController
from db_models.UserModel import RevokedTokenModel

from database_config import db
import os
#from config import DevelopmentConfig

application = Flask(__name__)
#application.config.from_object('config.DevelopmentConfig')
application.config['CORS_HEADERS'] = os.environ['CORS_HEADERS']
application.config['CORS_RESOURCES'] = os.environ['CORS_RESOURCES']
application.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ['SQLALCHEMY_TRACK_MODIFICATIONS']
application.config['JWT_BLACKLIST_ENABLED'] = os.environ['JWT_BLACKLIST_ENABLED']
application.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ['SQLALCHEMY_TRACK_MODIFICATIONS']
application.config['JWT_SECRET_KEY'] = os.environ['JWT_SECRET_KEY']
application.config['SECRET_KEY'] = os.environ['SECRET_KEY']

application.config['DEBUG'] = True

cors = CORS(application)
api = Api(application)

jwt = JWTManager(application)
db.init_app(application)


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return RevokedTokenModel.is_jti_blacklisted(jti)

@application.before_first_request
def create_tables():
    db.create_all()

@application.after_request
def after_request(response):
    
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,Origin,X-Requested-With,Accept,Accept-Language,Content-Language,Access-Control-Request-Headers,Access-Control-Request-Method,X-API-KEY')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    response.headers.add('Content-Type', 'application/json')
    return response

api.add_resource(AuthController.UserRegistration, '/registration')
api.add_resource(AuthController.UserLogin, '/login')
api.add_resource(AuthController.UserLogoutAccess, '/logout/access')
api.add_resource(AuthController.UserLogoutRefresh, '/logout/refresh')
api.add_resource(AuthController.TokenRefresh, '/token/refresh')
api.add_resource(AuthController.AllUsers, '/users')
api.add_resource(AuthController.SecretResource, '/secret')

api.add_resource(FileController.File, '/file') # Post request -> file upload, get request -> file download

api.add_resource(ImageController.SendImage, '/image')

api.add_resource(CourseController.Course, '/course')
api.add_resource(CourseController.AssignStudentToCourse, '/course/<int:course_id>') 

api.add_resource(SessionController.Session, '/session') # Post -> create session



@application.route('/')
def index():
    return jsonify({'message': 'Hello, World!'})

if __name__ == '__main__':
    application.run(debug=True)