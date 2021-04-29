from database_config import db
from flask import request, jsonify, make_response

class NoteModel(db.Model):
    __tablename__ = "notes"

    id = db.Column(db.Integer,primary_key = True, nullable=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), autoincrement=False)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'),  autoincrement=False)
    file_bytes = db.Column(db.LargeBinary, nullable=False)
    date = db.Column(db.String, nullable=False)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_student_id(cls, student_id):
        return cls.query.filter_by(student_id=student_id)

    @classmethod
    def return_info_by_student_id(cls, student_id):
        def to_json(x):
            return {
                'id': x.id,
                'course_id': x.course_id,
                'date': x.date
            }
        return {'notes': list(map(lambda x: to_json(x), cls.query.filter_by(student_id=student_id).all()))}

    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
        except:
            return {'message': 'Something went wrong'}