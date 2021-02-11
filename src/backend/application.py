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

application.config['MYSQL_HOST']='heredb.citwg2mji1tb.us-east-2.rds.amazonaws.com'
application.config['MYSQL_USER']='admin'
application.config['MYSQL_PASSWORD']='hereadmin'
application.config['MYSQL_DB']='here'
application.config['MYSQL_CURSORCLASS']='DictCursor'

mysql = MySQL(application)

@application.route('/')
def users():
    cursor = mysql.connection.cursor()
    try:
      cursor.execute('SELECT * FROM example')
      return str(cursor.fetchall())
    except Exception as e:
      print("Problem reading query")

if __name__ == '__main__':
    application.run(debug=True)