from flask_restful import Resource, reqparse
from flask import request
import base64
from PIL import Image
from ta.motion_tracking.analyze_image import analyze_image
import io
import sys
class SendImage(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('data')
    def post(self):
        data = self.parser.parse_args()
        #print("writing data", data['data'], file=sys.stdout)
        stringb64 = data['data']
        # sbuf = io.StringIO()
        # sbuf.write(data)
        # decode and convert into image
        stringb64 = stringb64.replace("data:image/png;base64,", "")
        im_bytes = base64.b64decode(stringb64)   # im_bytes is a binary image
        #print("BYTES", im_bytes, file=sys.stdout)
        im_file = io.BytesIO(im_bytes)  # convert image to file-like object
        print("IM_FILE", im_file, file=sys.stdout)
        pimg = Image.open(im_file)   # img is now PIL Image object
        pimg.show()
        print("size", pimg.size, file=sys.stdout)
        # converting RGB to BGR, as opencv standards
        # frame = cv2.cvtColor(np.array(pimg), cv2.COLOR_RGB2BGR)
        # Processing here
        analyze_image(pimg)
    def get(self):
        #TODO
        pass