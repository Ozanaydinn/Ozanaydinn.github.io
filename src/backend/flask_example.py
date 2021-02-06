from flask import Flask, render_template, flash, request, redirect, url_for, session, logging, url_for
from flask_socketio import SocketIO, emit
from flask_mysqldb import MySQL
import io
import base64
from PIL import Image
import numpy as np
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt

#Merhaba aaa
app = Flask(__name__)
app.secret_key = 'admin'
socketio = SocketIO(app)

# Config MySQL
app.config['MYSQL_HOST']='heredb.citwg2mji1tb.us-east-2.rds.amazonaws.com'
app.config['MYSQL_USER']='admin'
app.config['MYSQL_PASSWORD']='hereadmin'
app.config['MYSQL_DB']='here'
app.config['MYSQL_CURSORCLASS']='DictCursor'

# Init MYSQL
mysql = MySQL(app)

"""
try:
    cursor=mysql.connection.cursor()
    print("Mysql connection succesfull")
except ValueError:
    print("Error mysql connection")
"""
"""
@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')
"""
@app.route('/')
def users():
    cur = mysql.connection.cursor()
    print(cur)
    cur.execute('''SELECT * FROM example''')
    rv = cur.fetchall()
    return str(rv)

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
    app.run(debug=True)