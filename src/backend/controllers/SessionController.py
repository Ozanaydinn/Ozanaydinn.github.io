from flask_restful import Resource, reqparse
from flask import request
from db_models.SessionModel import SessionModel

class Session(Resource):
    parser = reqparse.RequestParser()

    @jwt_required
    def post(self):
        email = get_jwt_identity()
        current_user = UserModel.find_by_email(email)

        response = {
            "success": False,
            "id": -1
        }
        
        if current_user.type == 'instructor':
            session_model = SessionModel(instructor_id=current_user.id)
            res = session_model.save_to_db()
            if res['status']:
                response["id"] = res['id']
                response["success"] = True
        
        return response