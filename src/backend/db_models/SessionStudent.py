from database_config import db
from sqlalchemy.orm import relationship

class SessionStudent(db.Model):
    __tablename__ = "joins"

    session_id = db.Column(db.Integer, db.ForeignKey('sessions.id'), primary_key = True, autoincrement=False)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key = True, autoincrement=False)

    student = relationship('UserModel', backref='joins')
    session = relationship('SessionModel', backref='joins')

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