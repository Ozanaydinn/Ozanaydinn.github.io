from global_data import db
from sqlalchemy.orm import relationship

class CourseModel(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key = True, nullable=True)
    instructor_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String(120), nullable = False)
    slots = db.Column(db.String(120), nullable = False)

    inst = relationship('UserModel', backref='courses')

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_name_instructor(cls, name, instructor_id):
        return cls.query.filter_by(name = name, instructor_id = instructor_id).first()

    @classmethod
    def return_courses_of_instructor(cls, instructor_id):
        def to_json(x):
            return {
                'id': x.id,
                'name': x.name,
                'slots': x.slots
            }
        return {'courses': list(map(lambda x: to_json(x), cls.query.filter_by(instructor_id = instructor_id)))}

    @classmethod
    def return_course(cls, id):
        course = cls.query.filter_by(id=id).first()
        return {
            'id': course.id,
            'name': course.name,
            'slots': course.slots
        }
        

    @classmethod
    def return_all(cls):
        def to_json(x):
            return {
                'id': x.id,
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