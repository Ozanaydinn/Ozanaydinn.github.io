from flask import Flask, jsonify
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS


application = Flask(__name__)
application.config['CORS_HEADERS'] = 'Content-Type'
#application.config['CORS_RESOURCES'] = {r"/*": {"origins": "*"}}

cors = CORS(application, resources={r"/*": {"origins": "*"}})
#cors = CORS(application)
api = Api(application)

application.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://qmgznxoqxxasxm:90a4da8e5fffe0b52c91e758debe7f2183712734d72f186903334778211a9802@ec2-176-34-222-188.eu-west-1.compute.amazonaws.com:5432/d5a3te8g5fd7ha'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.config['SECRET_KEY'] = 'some-secret-string'
application.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
application.config['JWT_BLACKLIST_ENABLED'] = True
application.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

jwt = JWTManager(application)
db = SQLAlchemy(application)

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return models.RevokedTokenModel.is_jti_blacklisted(jti)

@application.before_first_request
def create_tables():
    db.create_all()

@application.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,Origin,X-Requested-With,Accept,Accept-Language,Content-Language,Access-Control-Request-Headers,Access-Control-Request-Method,X-API-KEY')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    #response.headers.add('Content-Type', 'application/json')
    return response


import models, auth, s3bucket, image, user_functions

api.add_resource(auth.UserRegistration, '/registration')
api.add_resource(auth.UserLogin, '/login')
api.add_resource(auth.UserLogoutAccess, '/logout/access')
api.add_resource(auth.UserLogoutRefresh, '/logout/refresh')
api.add_resource(auth.TokenRefresh, '/token/refresh')
api.add_resource(auth.AllUsers, '/users')
api.add_resource(auth.SecretResource, '/secret')

api.add_resource(s3bucket.FileUpload, '/upload')
api.add_resource(s3bucket.FileDownload, '/download')

api.add_resource(image.SendImage, '/image')

@application.route('/')
def index():
    return jsonify({'message': 'Hello, World!'})

if __name__ == '__main__':
    application.run(debug=True)