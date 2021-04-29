from flask_jwt_extended import ( create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity, jwt_refresh_token_required,
    get_raw_jwt
)
from flask_restful import Resource, reqparse
from db_models.FileModel import FileModel
from db_models.NoteModel import NoteModel
from db_models.UserModel import UserModel
from db_models.CourseModel import CourseModel
from flask import send_file


class File(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('file', help = 'This field cannot be blank', required = True)
    parser.add_argument('course_id', help = 'This field cannot be blank', required = True)

    @jwt_required
    def post(self):
        data = self.parser.parse_args()
        
        f = data['file'].replace("data:application/pdf;base64,", "")
        
        f = bytes(f, "utf-8")

        email = get_jwt_identity()
        
        file_model = FileModel(course_id=data['course_id'], file_bytes=f)

        return file_model.save_to_db()

    # File'ı çekmek için buraya get methodu yazın

class Note(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('file', help = 'This field cannot be blank', required = True)
    parser.add_argument('course_id', help = 'This field cannot be blank', required = True)

    @jwt_required
    def post(self):
        data = self.parser.parse_args()
        email = get_jwt_identity()
        current_user = UserModel.find_by_email(email)

        print(current_user.email)

        f = data['file'].replace("data:image/png;base64,", "")
        f = bytes(f, "utf-8")

        note_model = NoteModel(course_id=data['course_id'], student_id=current_user.id, file_bytes=f)
        return note_model.save_to_db()