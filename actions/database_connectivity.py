import sqlite3

conn = sqlite3.connect('data.db')

print("connected")

class Database:

  @staticmethod
  def initDb():
    conn.execute('''PRAGMA foreign_keys = 1''')
    conn.commit()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username VARCHAR(100) PRIMARY KEY,
            name VARCHAR(100) NOT NULL
        );
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            username VARCHAR(100) NOT NULL,
            category VARCHAR(50) NOT NULL,
            FOREIGN KEY (username) REFERENCES users(username),
            PRIMARY KEY (username,category)
        );
    ''')
    conn.execute('''
        CREATE TABLE activities (
            username VARCHAR(100) NOT NULL,
            activity VARCHAR(100) NOT NULL,
            category VARCHAR(50) NOT NULL,
            deadline TIME(0) NOT NULL,
            completed BOOLEAN NOT NULL,
            FOREIGN KEY (username, category) REFERENCES categories(username,category)
        );
    ''')
    conn.commit()

  @staticmethod
  def createUser(username, name):
    try:
      conn.execute('''
        INSERT INTO users (username, name) VALUES (?, ?);
      ''', (username, name))
      conn.commit()
      print("User inserted")
      return True
    except sqlite3.IntegrityError as e :
        print("Problem!",e)
        return False

  @staticmethod
  def insertItem(username, activity ,category,deadline):

    try:
      conn.execute('''
      INSERT INTO activities (username, activity, category,deadline,completed) VALUES (?, ?, ?,?,?);
    ''', (username, activity ,category,deadline,False))
      conn.commit()
      return True
    except sqlite3.IntegrityError:
        return False


  @staticmethod
  def selectItems(username, category=None):


    cur = conn.cursor()
    if category == None:
      cur.execute('''
      SELECT * FROM activities WHERE username == (?);
      ''',(username,))
    else:
      cur.execute('''
      SELECT * FROM activities WHERE username == ? AND category == ?;
      ''',(username,category))

    rows = cur.fetchall()

    return str(rows).strip('[]') if len(rows) > 0 else "No activity found"

  @staticmethod
  def deleteItem(username, activity ,category,deadline):

    conn.execute('''
      DELETE FROM activities WHERE username == ? AND activity == ? AND category == ? AND deadline == ?
    ''', (username, activity ,category,deadline))

    conn.commit()


  @staticmethod
  def insertCategory(username, category):
    try:
      conn.execute('''
        INSERT INTO categories (username, category) VALUES (?,?);
      ''', (username,category))
      conn.commit()
      return True
    except sqlite3.IntegrityError:
        return False
    


  @staticmethod
  def selectCategories(username):

    cur = conn.cursor()
    cur.execute('''
    SELECT * FROM categories WHERE username == (?);
    ''',username) 

    rows = cur.fetchall()

    return str(rows).strip('[]') if len(rows) > 0 else "No activity found"

  @staticmethod
  def deleteCategory(username, category):

    conn.execute('''
      DELETE FROM categories WHERE username == ? AND category == ? 
    ''', (username, category))

    conn.commit()

    
  @staticmethod
  def setItemStatus(username, activity ,category,deadline,completed):

    conn.execute('''
      UPDATE activities SET completed = ? WHERE username == ? AND activity == ? AND category == ? AND deadline == ?
    ''', (completed, username, activity ,category,deadline))
    conn.commit()


  @staticmethod
  def DataUpdate(facility_type,location):
      
      c = conn.cursor()
      print(facility_type,location)
      sql = "CREATE TABLE test2 (facility_type VARCHAR(255),location VARCHAR(255))"
      sql2 = 'INSERT INTO test2 (facility_type,location) VALUES ("{0}","{1}");'.format(facility_type,location)
      sql3 = 'SELECT * FROM test2'
      sql1 = 'SELECT * FROM test'

      print("prima di fetchall")
      c.execute(sql3)
      print(c.fetchall())
      c.execute(sql1)
      print(c.fetchall())
      conn.commit()
      conn.close()