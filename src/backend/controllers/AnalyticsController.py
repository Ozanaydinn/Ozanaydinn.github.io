from flask_restful import Resource, reqparse
from backend.models.user import User
import db_models.SessionStudent as SessionStudent

from flask_jwt_extended import ( create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity, jwt_refresh_token_required,
    get_raw_jwt
)

current_students = {"123": User("123", "12345")}

class HandResult(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('hand_result', help = 'This field cannot be blank')

    def post(self):
        data = self.parser.parse_args()
        email = get_jwt_identity()
        current_user = User.UserModel.find_by_email(email)

        #first, record the hand result in the user array for later use in analytics
        current_students[current_user.id].handResults.append(data['hand_result'])

        # Second, if hand result is 5 or 1, assume that the student raises their hands, update notification
        if data['hand_result']['number'] == 5 or data['hand_result']['number'] == 1: #TODO add thumb=unknown state as well
            notification = current_user.username + " raised their hand!"
            result = SessionStudent.update_notification(current_user.id, notification)
            return result

"""
May not be necessary, check later
"""
class FacePoseResult(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('head_pose', help = 'This field cannot be blank')

    def post(self):
        data = self.parser.parse_args()
        email = get_jwt_identity()
        current_user = User.UserModel.find_by_email(email)

        # first, add the head result to the user array
        current_students[current_user.id].headPoses.append(data['head_pose'])

        #check if we have gathered enough samples, and that the user are distracted in half of them
        array_length = len(current_students[current_user.id].headPoses)
        if  array_length % 12 == 0 and array_length != 0:
            if current_students[current_user.id].headPoses.count("straight") <= array_length / 2:
                notification = "You seem distracted, is everything okay?"
                result = SessionStudent.update_notification(current_user.id, notification)
                return result

class PhoneResult(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("phone_result", help = 'This field cannot be blank')

    def post(self):
        data = self.parser.parse_args()
        email = get_jwt_identity()
        current_user = User.UserModel.find_by_email(email)

        # first, add the head result to the user array
        current_students[current_user.id].phoneResult.append(data['phone_result'])

        # check how many times a phone has been spotted in a minute
        array_length = len(current_students[current_user.id].headPoses)
        if  array_length % 12 == 0 and array_length != 0:
            if current_students[current_user.id].phoneResult.count("yes") >= array_length / 4:
                notification = "Looking at your phone often can distract you."
                result = SessionStudent.update_notification(current_user.id, notification)
                return result

def alertTeacherforDistraction():
    distractionCount = 0.0
    student_no = float(len(current_students))
    for student in current_students:
        if student.headPoses.count("straight") < ((len(student.headPoses) * 6)/10) or student.phoneResult.count("yes") > 2:
            distractionCount += 1

    if distractionCount / student_no > 0.7:
        notification = "Most of your students are distracted, might want to take a break."
        result = Se


class Analytics(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('hand_result', help = 'This field cannot be blank')
    parser.add_argument('head_pose', help = 'This field cannot be blank')

    def post(self):
        data = self.parser.parse_args()
        email = get_jwt_identity()
        current_user = User.UserModel.find_by_email(data['email'])