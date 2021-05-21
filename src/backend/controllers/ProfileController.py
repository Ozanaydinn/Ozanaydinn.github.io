from flask_restful import Resource, reqparse
import db_models.UserModel as User
from flask_jwt_extended import ( create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity, jwt_refresh_token_required,
    get_raw_jwt
)

class ChangeProfile(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', required=False)
    parser.add_argument('new_password', required=False)

    @jwt_required
    def post(self):
        data = self.parser.parse_args()
        email = get_jwt_identity()
        current_user = User.UserModel.find_by_email(email)
        resp = {'username': "", "password": ""}
        if data['username'] == None and data['old_password'] == None and data['new_password'] == None:
            return "Please enter a value!"

        # if username argument is given, change username
        if data['username'] != "":
            current_user.username = data['username']
            current_user.save_to_db()
            resp['username'] = "Username successfully changed!"

        if data['new_password'] != "":
            current_user.password = User.UserModel.generate_hash(data['new_password'])
            current_user.save_to_db()
            resp['password'] = "Password successfully changed!"

        return resp