from flask_restful import Resource, reqparse
from flask import request
import base64
from PIL import Image
from analyze_head import analyze_head
import io
import sys
class SendImage(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('data')
    
    def post(self):
        data = self.parser.parse_args()
        stringb64 = data['data']
        
        stringb64 = stringb64.replace("data:image/png;base64,", "")
        im_bytes = base64.b64decode(stringb64) 

        im_file = io.BytesIO(im_bytes)  
        pimg = Image.open(im_file)   
   
        result = analyze_head(pimg)
        
        return result