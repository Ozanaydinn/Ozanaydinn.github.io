from config import db
from sqlalchemy.orm import relationship

class CourseModel(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key = True, nullable=True)
    instructor = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String(120), nullable = False)
    slots = db.Column(db.String(120), nullable = False)

    inst = relationship('UserModel', backref='courses')

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_name_instructor(cls, name, instructor):
        return cls.query.filter_by(name = name, instructor = instructor).first()

    @classmethod
    def return_courses_of_instructor(cls, instructor):
        def to_json(x):
            return {
                'name': x.name,
            }
        return {'courses': list(map(lambda x: to_json(x), cls.query.filter_by(instructor = instructor)))}

    @classmethod
    def return_all(cls):
        def to_json(x):
            return {
                'name': x.name,
            }
        return {'courses': list(map(lambda x: to_json(x), CourseModel.query.all()))}

    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
        except:
            return {'message': 'Something went wrong'}