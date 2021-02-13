from flask import Flask, render_template, flash, request, redirect, url_for, session, logging, url_for, send_file
from flask_socketio import SocketIO, emit
from flask_mysqldb import MySQL
import io
import base64
from PIL import Image
import numpy as np
import DatabaseConnector
from s3_buckets import upload_file, download_file, list_files
import os

application = Flask(__name__)
application .secret_key = 'admin'
socketio = SocketIO(application)
UPLOAD_FOLDER = "uploads"
BUCKET = "heredrive"

# Config DB
db = DatabaseConnector.DatabaseConnector(application, 'heredb.citwg2mji1tb.us-east-2.rds.amazonaws.com',
                        'admin', 'hereadmin', 'here')

"""
@application.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')
"""
@application.route('/')
def users():
    print("hello")
    output = db.read_query('SELECT * FROM example')
    return str(output ) + "hello"


@application.route("/upload", methods=['POST'])
def upload():
    if request.method == "POST":
        f = request.files['file']
        f.save(os.path.join(UPLOAD_FOLDER, f.filename))
        upload_file(f"uploads/{f.filename}", BUCKET)

@application.route("/download/<filename>", methods=['GET'])
def download(filename):
    if request.method == 'GET':
        output = download_file(filename, BUCKET)

        return send_file(output, as_attachment=True)

"""
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
    
"""



if __name__ == '__main__':
    application.run(debug=True)