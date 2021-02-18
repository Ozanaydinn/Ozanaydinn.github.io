from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import io
import base64
import re
from PIL import Image
import numpy as np

#Merhaba aaa
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')

@socketio.on('image')
def image(data):
    # sbuf = io.StringIO()
    # sbuf.write(data)

    # decode and convert into image
    data = data.replace("data:image/png;base64,", "")
    im_bytes = base64.b64decode(data)   # im_bytes is a binary image
    im_file = io.BytesIO(im_bytes)  # convert image to file-like object
    pimg = Image.open(im_file)   # img is now PIL Image object
    pimg.show()

    # converting RGB to BGR, as opencv standards
    # frame = cv2.cvtColor(np.array(pimg), cv2.COLOR_RGB2BGR)

    # Processing here

if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port="8080")