from flask_mysqldb import MySQL

class DatabaseConnector:
  def __init__(self, application, host, user, password, db_name):
    self.host = host
    self.user = user
    self.password = password
    self.db_name = db_name

    self.config_db(application)

    self.mysql = MySQL(application)
    self.cursor = self.mysql.connection.cursor()

  def config_db(self, application):
    application.config['MYSQL_HOST']=self.host
    application.config['MYSQL_USER']=self.user
    application.config['MYSQL_PASSWORD']=self.password
    application.config['MYSQL_DB']=self.db_name
    application.config['MYSQL_CURSORCLASS']='DictCursor'

  def read_query(self, query):
    try:
      self.cursor.execute(query)
      return self.cursor.fetchall()
    except Exception as e:
      print("Problem reading query")
    
  def execute_query(self, query):
    try:
      self.cursor.execute(query)
      self.mysql.connection.commit()
    except Exception as e:
      print("Problem reading query")