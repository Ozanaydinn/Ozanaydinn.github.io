from flask import Flask, jsonify
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager


application = Flask(__name__)
api = Api(application)

application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:hereadmin@heredb.citwg2mji1tb.us-east-2.rds.amazonaws.com:3306/here'
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

import models, auth, s3bucket, image

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