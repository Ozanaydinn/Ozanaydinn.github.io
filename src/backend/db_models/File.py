from database_config import db
from sqlalchemy.orm import relationship

class File(db.Model):
    __tablename__ = "files"

    id = db.Column(db.Integer, primary_key = True, nullable=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    file_bytes = db.Column(db.LargeBinary, nullable=False)

    def save_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
            return {'message': "File successfully added to the files table", 'status': True}
        except:
            return {'message': 'Something went wrong', 'status': False}


    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
        except:
            return {'message': 'Something went wrong'}