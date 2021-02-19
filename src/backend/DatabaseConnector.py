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

  def read_query(self, query):
    cursor = self.mysql.connection.cursor()
    try:
      cursor.execute(query)
      return cursor.fetchall()
    except Exception as e:
      print("Problem reading query")
    
  def execute_query(self, query, values):
    cursor = self.mysql.connection.cursor()
    try:
      cursor.execute(query, values)
      self.mysql.connection.commit()
    except Exception as e:
      print("Problem reading query")

  def register_user(self, username, password, email):
    cursor = self.mysql.connection.cursor()
    reg_query = "INSERT INTO user(username, password, email) VALUES(%s,%s,%s)"
    values = (username, password, email)

    #try:
    cursor.execute(reg_query, values)
    self.mysql.connection.commit()

    cursor.execute("SELECT user_id FROM user WHERE username = %s", (username,))
    user = cursor.fetchone()
    id = user['user_id']
    return id
    #except Exception as e:
    #  print("Problem reading query")

  def register_student(self, id):
    cursor = self.mysql.connection.cursor()
    cursor.execute("INSERT INTO student(student_id) VALUES({0})".format(id))
    self.mysql.connection.commit()

  def register_instructor(self, id):
    cursor = self.mysql.connection.cursor()
    cursor.execute("INSERT INTO instructor(instructor_id) VALUES({0})".format(id))
    self.mysql.connection.commit()

  def login_user(self, username):
    cursor = self.mysql.connection.cursor()
    count = cursor.execute("SELECT password FROM user WHERE username = %s", (username,))
    
    if count > 0:
      user = cursor.fetchone()
      return user['password']
    else:
      return -1

  def executeScriptsFromFile(self, filename, cursor):
    # Open and read the file as a single buffer
    fd = open(filename, 'r')
    sqlFile = fd.read()
    fd.close()

    # all SQL commands (split on ';')
    sqlCommands = sqlFile.split(';')

    # Execute every command from the input file
    for command in sqlCommands:
        cursor.execute(command)