from flask_restful import Resource, reqparse
import base64
from PIL import Image

class SendImage(Resource):
    def post(self):
        return "request geldiii"
        # sbuf = io.StringIO()
        # sbuf.write(data)

        # decode and convert into image
        """
        data = data.replace("data:image/png;base64,", "")
        im_bytes = base64.b64decode(data)   # im_bytes is a binary image
        im_file = io.BytesIO(im_bytes)  # convert image to file-like object
        pimg = Image.open(im_file)   # img is now PIL Image object
        pimg.show()
        """
        # converting RGB to BGR, as opencv standards
        # frame = cv2.cvtColor(np.array(pimg), cv2.COLOR_RGB2BGR)

        # Processing here

    def get(self):
        #TODO
        pass


    def options(self):
        return {'Allow' : 'PUT' }, 200, \
        { 'Access-Control-Allow-Origin': '*', \
        'Access-Control-Allow-Methods' : 'PUT,GET' }