from database_config import db
from flask import request, jsonify, make_response

class NoteModel(db.Model):
    __tablename__ = "notes"

    id = db.Column(db.Integer,primary_key = True, nullable=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), autoincrement=False)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'),  autoincrement=False)
    file_bytes = db.Column(db.LargeBinary, nullable=False)

    def save_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
            return make_response(jsonify({"Note added successfully!"}), 200)
        except:
            return make_response(jsonify({"error":"Can't add note to db."}), 404)

    @classmethod
    def find_by_student_id(cls, student_id):
        return cls.query.filter_by(student_id=student_id)

    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
        except:
            return {'message': 'Something went wrong'}