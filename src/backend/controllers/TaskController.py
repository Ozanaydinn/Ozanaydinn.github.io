from flask_jwt_extended import ( create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity, jwt_refresh_token_required,
    get_raw_jwt
)
from flask import jsonify, make_response
from flask_restful import Resource, reqparse
from models.tasks import analyze_hand, analyze_head
from celery.result import AsyncResult
from db_models.SessionStudent import SessionStudent
from db_models.UserModel import UserModel
from controllers.AnalyticsController import AnalyticsController


class Hand(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('data', help='This field cannot be blank', required=True)

    @jwt_required
    def post(self):
        data = self.parser.parse_args()
        email = get_jwt_identity()
        current_user = UserModel.find_by_email(email)

        joins = SessionStudent.find_by_student_id(current_user.id)
        
        task = analyze_hand.delay(image_data=data['data'], session_id=joins.session_id, user_id=current_user.id)

        return make_response(jsonify({"task_id": task.id}), 202)

class Head(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('data', help='This field cannot be blank', required=True)
    parser.add_argument('timestamp', help='This field cannot be blank', required=True)

    @jwt_required
    def post(self):
        data = self.parser.parse_args()
        email = get_jwt_identity()
        current_user = UserModel.find_by_email(email)

        joins = SessionStudent.find_by_student_id(current_user.id)
        
        task = analyze_head.delay(image_data=data['data'], session_id=joins.session_id, user_id=current_user.id, timestamp=data['timestamp'])

        return make_response(jsonify({"task_id": task.id}), 202)

class TaskResult(Resource):
    def get(self, task_id=None):
        
        if not task_id:
            return make_response(jsonify({"error": "You have to specify a task id!"}), 400)

        task_result = AsyncResult(task_id)

        data = {
                "session_id": task_result.result["session_id"],
                "user_id": task_result.result["user_id"]
            }

        result = ""

        if "hand_result" in task_result.result:
            data["hand_result"] =task_result.result["hand_result"]

            result = AnalyticsController.analyze_hand_result(data)
        elif "head_pose_result" in task_result.result:
            data["head_pose_result"] = task_result.result["head_pose_result"]
            data["timestamp"] = task_result.result["timestamp"]

            result = AnalyticsController.analyze_head_result(data)
        elif "phone_result" in task_result.result:
            data["phone_result"] =task_result.result["phone_result"]
              
            result = AnalyticsController.analyze_phone(data)

        return make_response(jsonify(result), 200)