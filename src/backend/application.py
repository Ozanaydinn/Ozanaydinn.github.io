from flask import Flask, render_template, flash, request, redirect, url_for, session, logging, url_for
from flask_socketio import SocketIO, emit
from flask_mysqldb import MySQL
import io
import base64
from PIL import Image
import numpy as np
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
import DatabaseConnector

application = Flask(__name__)
application .secret_key = 'admin'
socketio = SocketIO(application)

# Config DB
db = DatabaseConnector.DatabaseConnector(application, 'heredb.citwg2mji1tb.us-east-2.rds.amazonaws.com',
                        'admin', 'hereadmin', 'here')

db_connection = db.connect()

"""
@application.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')
"""
@application.route('/')
def users():
    output = db.read_query(db_connection, 'SELECT * FROM example')
    return str(output)
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