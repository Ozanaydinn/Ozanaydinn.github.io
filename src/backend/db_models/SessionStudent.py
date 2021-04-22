from database_config import db
from sqlalchemy.orm import relationship

class SessionStudent(db.Model):
    __tablename__ = "joins"

    session_id = db.Column(db.Integer, db.ForeignKey('sessions.id', ondelete='CASCADE'), primary_key = True, autoincrement=False)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key = True, autoincrement=False)


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
        except:
            return {'message': 'Something went wrong'}

    @classmethod
    def delete(cls, student_id):
        try: 
            db.session.query(cls).filter_by(student_id = student_id).delete()
            db.session.commit()
            return {'message': 'Student deleted from session.'}
        except:
            return {'message': 'Something went wrong.'}

    @classmethod
    def delete(cls, student_id):
        try: 
            db.session.query(cls).filter_by(student_id = student_id).delete()
            db.session.commit()
            return {'message': 'Student deleted from session.'}
        except:
            return {'message': 'Something went wrong.'}
