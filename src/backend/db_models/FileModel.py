from global_data import db
from sqlalchemy.orm import relationship

class FileModel(db.Model):
    __tablename__ = "files"

    id = db.Column(db.Integer, primary_key = True, nullable=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    file_url = db.Column(db.String(120), nullable=False)

    def save_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
            return {'message': "File successfully added to the files table", 'status': True}
        except:
            return {'message': 'Something went wrong', 'status': False}

    @classmethod
    def find_with_course_id(cls, course_id):
        return cls.query.filter_by(course_id=course_id).first()


    @classmethod
    def delete_with_course_id(cls, course_id):
        try: 
            db.session.query(cls).filter_by(course_id = course_id).delete()
            db.session.commit()
            return {'message': 'File deleted.'}
        except:
            return {'message': 'Something went wrong'}


    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
        except:
            return {'message': 'Something went wrong'}