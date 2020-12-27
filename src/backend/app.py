from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import io
import base64
import cv2
from PIL import Image
import numpy as np

#Merhaba aaa
app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')

@socketio.on('image')
def image(data):
    sbuf = io.StringIO()
    sbuf.write(data)

    # decode and convert into image
    b = io.BytesIO(base64.b64decode(data))
    pimg = Image.open(b)

    # converting RGB to BGR, as opencv standards
    frame = cv2.cvtColor(np.array(pimg), cv2.COLOR_RGB2BGR)

    # Processing here

if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1')