from application import db
from passlib.hash import pbkdf2_sha256 as sha256
from sqlalchemy.orm import relationship

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(120), nullable = False)
    password = db.Column(db.String(120), nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    type = db.Column(db.String(120), nullable = False)
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)
    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email = email).first()

    @classmethod
    def return_all(cls):
        def to_json(x):
            return {
                'username': x.username,
                'password': x.password,
                'email': x.email,
                'type': x.type
            }
        return {'users': list(map(lambda x: to_json(x), UserModel.query.all()))}

    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
        except:
            return {'message': 'Something went wrong'}

class RevokedTokenModel(db.Model):
    __tablename__ = 'revoked_tokens'
    id = db.Column(db.Integer, primary_key = True)
    jti = db.Column(db.String(120))
    
    def add(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti = jti).first()
        return bool(query)


class CourseModel(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key = True, nullable=True)
    instructor = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String(120), nullable = False)
    slots = db.Column(db.String(120), nullable = False)

    inst = relationship('UserModel', backref='courses')
    files = relationship('File', backref='courses')

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

class CourseStudent(db.Model):
    __tablename__ = "takes"

    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), primary_key = True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key = True)

    student = relationship('UserModel', backref='takes')
    course = relationship('CourseModel', backref='takes')

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

class File(db.Model):
    __tablename__ = "files"

    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), primary_key=True)
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
