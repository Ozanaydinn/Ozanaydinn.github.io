from flask_mysqldb import MySQL

class DatabaseConnector:
  def __init__(self, application, host, user, password, db_name):
    self.host = host
    self.user = user
    self.password = password
    self.db_name = db_name

    self.config_db(application)

    self.mysql = MySQL(application)

  def config_db(self, application):
    application.config['MYSQL_HOST']=self.host
    application.config['MYSQL_USER']=self.user
    application.config['MYSQL_PASSWORD']=self.password
    application.config['MYSQL_DB']=self.db_name
    application.config['MYSQL_CURSORCLASS']='DictCursor'

  def connect(self):
    try:
      connection=self.mysql.connect()
      print("Mysql connection succesfull")
    except ValueError:
      print("Error mysql connection")
    return connection

  def read_query(self, connection, query):
    cursor = connection.cursor()
    try:
      cursor.execute(query)
      return cursor.fetchall()
    except Exception as e:
      print("Problem reading query")
    
  def execute_query(self, connection, query):
    cursor = connection.cursor()
    try:
      cursor.execute(query)
      connection.commit()
    except Exception as e:
      print("Problem reading query")