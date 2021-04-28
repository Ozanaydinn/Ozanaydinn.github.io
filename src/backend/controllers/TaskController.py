from flask import jsonify, make_response
from flask_restful import Resource, reqparse
from models.tasks import analyze_hand
from models.tasks import analyze_head
from celery.result import AsyncResult

class Hand(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('data', help='This field cannot be blank', required=True)

    def post(self):
        data = self.parser.parse_args()
        
        task = analyze_hand.delay(data['data'])

        return make_response(jsonify({"task_id": task.id}), 202)

class Head(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('data', help='This field cannot be blank', required=True)

    def post(self):
        data = self.parser.parse_args()
        
        task = analyze_head.delay(data['data'])

        return make_response(jsonify({"task_id": task.id}), 202)

class TaskResult(Resource):
    def get(self, task_id=None):
        
        if not task_id:
            return make_response(jsonify({"error": "You have to specify a task id!"}), 400)

        task_result = AsyncResult(task_id)

        result = {
            "task_id": task_id,
            "task_status": task_result.status,
            "task_result": task_result.result
        }

        return make_response(jsonify(result), 200)