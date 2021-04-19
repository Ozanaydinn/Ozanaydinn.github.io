from database_config import db
from sqlalchemy.orm import relationship

class SessionModel(db.Model):
    __tablename__ = 'sessions'

    id = db.Column(db.Integer, primary_key = True, nullable=True)
    instructor_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def save_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
            return {'status': True,
            'id': self.id}
        except:
            return {'status': False}

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
    def delete(cls, id):
        # TO DO
        pass