from flask_jwt_extended import ( create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity, jwt_refresh_token_required,
    get_raw_jwt
)
from flask_restful import Resource, reqparse
import boto3
import os
from flask import send_file


class FileUpload(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('file', help = 'This field cannot be blank', required = True)

    @jwt_required
    def post(self):
        data = self.parser.parse_args()
        f = data['file']
        f.save(os.path.join("uploads", f.filename))
        s3_client = boto3.client('s3')
        response = s3_client.upload_file(f.filename, "heredrive", f.filename)

        return response

class FileDownload(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('file', help = 'This field cannot be blank', required = True)

    @jwt_required
    def get(self):
        data = self.parser.parse_args()
        f = data['file']
        s3 = boto3.resource('s3')
        output = f"downloads/{f.file_name}"
        s3.Bucket("heredrive").download_file(f.filename, output)

        return send_file(output, as_attachment=True)