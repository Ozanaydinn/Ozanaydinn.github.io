from flask_jwt_extended import ( create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity, jwt_refresh_token_required,
    get_raw_jwt
)
from flask_restful import Resource, reqparse, request
from db_models.FileModel import FileModel
from db_models.NoteModel import NoteModel
from db_models.UserModel import UserModel
from db_models.CourseModel import CourseModel
from flask import send_file

import base64


class File(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('file', help = 'This field cannot be blank', required = True)
    parser.add_argument('course_id', help = 'This field cannot be blank', required = True)

    def post(self):
        data = self.parser.parse_args()

        course_id = data["course_id"]
        
        f = data['file'].replace("data:application/pdf;base64,", "")
        f = bytes(f, "utf-8")

        FileModel.delete_with_course_id(course_id)
        file_model = FileModel(course_id=course_id, file_bytes=f)
        return file_model.save_to_db()

    def get(self):
        course_id = request.args.get("course_id")

        f = FileModel.find_with_course_id(course_id).file_bytes

        resp = {
            "file": f.decode('utf-8')
        }
        
        return resp

class Note(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('file', help = 'This field cannot be blank', required = True)
    parser.add_argument('course_id', help = 'This field cannot be blank', required = True)
    parser.add_argument('date', help = 'This field cannot be blank', required = True)

    @jwt_required
    def post(self):
        data = self.parser.parse_args()
        email = get_jwt_identity()
        current_user = UserModel.find_by_email(email)

        f = data['file'].replace("data:image/png;base64,", "")
        f = bytes(f, "utf-8")

        note_model = NoteModel(course_id=data['course_id'], student_id=current_user.id, file_bytes=f, date=data['date'])
        return note_model.save_to_db()

    @jwt_required
    def get(self):
        email = get_jwt_identity()
        current_user = UserModel.find_by_email(email)

        data = NoteModel.return_info_by_student_id(current_user.id)

        notes = {}
        for note in data['notes']:
            if note['course_id'] not in notes:
                notes[note['course_id']] = []
                notes[note['course_id']].append({
                    "id": note["id"],
                    "date": note["date"],
                    "course_id": note["course_id"]
                })
            else:
                notes[note['course_id']].append({
                    "id": note["id"],
                    "date": note["date"],
                    "course_id": note["course_id"]
                })
        
        output_notes = {}
        for course in notes:
            courseModel = CourseModel.find_by_id(course)
            output_notes[courseModel.name] = notes[course]

        return output_notes
        
class SingleNote(Resource):
    @jwt_required
    def get(self, note_id):
        note = NoteModel.find_by_id(note_id)
        bts = note.file_bytes

        return bts.decode('utf-8')