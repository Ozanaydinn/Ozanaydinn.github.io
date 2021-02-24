from flask_restful import Resource, reqparse
import base64
from PIL import Image
import io

class SendImage(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('image', help = 'This field cannot be blank', required = True)
    def post(self):
        data = self.parser.parse_args()
        # sbuf = io.StringIO()
        # sbuf.write(data)

        # decode and convert into image
        bs64 = str(data["image"])
        bs64 = bs64.replace("data:image/png;base64,", "")
        im_bytes = base64.b64decode(bs64)   # im_bytes is a binary image
        im_file = io.BytesIO(im_bytes)  # convert image to file-like object
        pimg = Image.open(im_file)   # img is now PIL Image object
        pimg.show()
        
        # converting RGB to BGR, as opencv standards
        # frame = cv2.cvtColor(np.array(pimg), cv2.COLOR_RGB2BGR)

        # Processing here
        return data

    def get(self):
        #TODO
        pass