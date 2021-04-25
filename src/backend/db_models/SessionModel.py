from database_config import db
from sqlalchemy.orm import relationship

class SessionModel(db.Model):
    __tablename__ = 'sessions'

    id = db.Column(db.Integer, primary_key = True, nullable=True)
    instructor_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    notification = db.Column(db.String(120))
    socket_id = db.Column(db.String(32))

    students = relationship('SessionStudent', backref='sessions', passive_deletes=True)

    def save_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
            return {'status': True,
            'id': self.id}
        except:
            return {'status': False}
    
    @classmethod
    def find_by_instructor_id(cls, instructor_id):
        return cls.query.filter_by(instructor_id=instructor_id).first()

    @classmethod
    def return_all(cls):
        def to_json(x):
            return {
                'id': x.id,
            }
        return {'sessions': list(map(lambda x: to_json(x), SessionModel.query.all()))}

    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
        except:
            return {'message': 'Something went wrong'}

    @classmethod
    def delete(cls, instructor_id):
        try: 
            db.session.query(cls).filter_by(instructor_id = instructor_id).delete()
            db.session.commit()
            return {'message': 'Session deleted.'}
        except:
            return {'message': 'Something went wrong'}

    @classmethod
    def update_notification(cls, instructor_id, notification):
        try:
            ses = db.session.query(cls).filter_by(instructor_id = instructor_id).first()
            ses.notification = notification
            db.session.commit()
            return {'message': 'Instructor notification updated.'}
        except:
            return {'message': 'Something went wrong.'}
