from flask_jwt_extended import ( create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity, jwt_refresh_token_required,
    get_raw_jwt
)
from flask_restful import Resource, reqparse
from db_models.File import File
from db_models.UserModel import UserModel
from db_models.CourseModel import CourseModel
import boto3
import os
from flask import send_file


class File(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('file', help = 'This field cannot be blank', required = True)
    parser.add_argument('course_name', help = 'This field cannot be blank', required = True)

    @jwt_required
    def post(self):
        data = self.parser.parse_args()
        
        f = data['file'].replace("data:application/pdf;base64,", "")

        f = bytes(f, "utf-8")

        course_name = data['course_name']

        email = get_jwt_identity()
        
        current_user = UserModel.find_by_email(email)

        course = CourseModel.find_by_name_instructor(course_name, current_user.id)

        file_model = File(course_id=course.id, file_bytes=f)

        return file_model.save_to_db()

    # File'ı çekmek için buraya get methodu yazın
