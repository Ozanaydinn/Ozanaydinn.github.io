from flask_restful import Resource, reqparse
import models.User as User
from flask_jwt_extended import ( create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity, jwt_refresh_token_required,
    get_raw_jwt
)

class Analytics(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('hand_result', help = 'This field cannot be blank')
    parser.add_argument('head_pose', help = 'This field cannot be blank')

    def post(self):
        data = self.parser.parse_args()
        email = get_jwt_identity()
        current_user = User.UserModel.find_by_email(data['email'])