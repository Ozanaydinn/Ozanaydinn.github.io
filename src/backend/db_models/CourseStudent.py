from database_config import db
from sqlalchemy.orm import relationship

class CourseStudent(db.Model):
    __tablename__ = "takes"

    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), primary_key = True, autoincrement=False)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key = True, autoincrement=False)

    student = relationship('UserModel', backref='takes')
    course = relationship('CourseModel', backref='takes')

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def return_courses_of_student(cls, student_id):
        def to_json(x):
            return {
                'id': x.course_id
            }
        return {'courses': list(map(lambda x: to_json(x), cls.query.filter_by(student_id = student_id)))}

    @classmethod
    def return_students_of_course(cls, course_id):
        def to_json(x):
            return {
                'id': x.student_id
            }
        return {'courses': list(map(lambda x: to_json(x), cls.query.filter_by(course_id = course_id)))}

    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
        except:
            return {'message': 'Something went wrong'}