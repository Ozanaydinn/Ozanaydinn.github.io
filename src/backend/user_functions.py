from flask_jwt_extended import ( create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity, jwt_refresh_token_required,
    get_raw_jwt
)
from models import UserModel, CourseModel, CourseStudent, RevokedTokenModel
from flask_restful import Resource, reqparse

class AssignStudentToCourse(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('student_email', help = 'This field cannot be blank', required = True)
    parser.add_argument('course_name', help = 'This field cannot be blank', required = True)

    @jwt_required
    def post(self):
        data = self.parser.parse_args()
        email = get_jwt_identity()
        current_user = UserModel.find_by_email(email)

        course = CourseModel.find_by_name_instructor(data['course_name'], current_user.id)
        student = UserModel.find_by_email(data['student_email'])

        assign = CourseStudent(
            course_id = course.id,
            student_id = student.id
        )
        try:
            assign.save_to_db()
            return {
                'message': 'Assigned.'
            }
        except:
            return {'message': 'Something went wrong'}, 500



class Course(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('course_name', help = 'This field cannot be blank', required = True)
    parser.add_argument('slots', help = 'This field cannot be blank', required = True)

    @jwt_required
    def post(self):
        data = self.parser.parse_args()
        email = get_jwt_identity()
        current_user = UserModel.find_by_email(email)

        new_course = CourseModel(
            instructor = current_user.id,
            name = data['course_name'],
            slots = data['slots']
        )

        try:
            new_course.save_to_db()
            return {
                'message': 'Course {} was created'.format( data['course_name'])
            }
        except:
            return {'message': 'Something went wrong'}, 500

    @jwt_required
    def get(self):
        email = get_jwt_identity()
        current_user = UserModel.find_by_email(email)
        return CourseModel.return_courses_of_instructor(current_user.id)
