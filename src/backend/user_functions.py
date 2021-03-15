from flask_jwt_extended import ( create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity, jwt_refresh_token_required,
    get_raw_jwt
)
from flask_restful import Resource, reqparse

class assignStudentToCourse(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('file', help = 'This field cannot be blank', required = True)

    @jwt_required
    def post(self):
        data = self.parser.parse_args()
        f = data['file']
        f.save(os.path.join("uploads", f.filename))
        s3_client = boto3.client('s3')
        response = s3_client.upload_file(f.filename, "heredrive", f.filename)