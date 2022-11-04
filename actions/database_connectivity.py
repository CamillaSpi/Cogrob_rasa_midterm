import sqlite3
import hashlib

conn = sqlite3.connect('data.db')
cur = conn.cursor()

print("connected")

class Database:

  @staticmethod
  def initDb():
    conn.execute('''PRAGMA foreign_keys = 1''')
    conn.commit()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username VARCHAR(100) PRIMARY KEY
        );
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            username VARCHAR(100) NOT NULL,
            category VARCHAR(50) NOT NULL,
            FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE ON UPDATE CASCADE,
            PRIMARY KEY (username,category)
        );
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS activities (
            id_activity VARCHAR(256) NOT NULL,
            username VARCHAR(100) NOT NULL,
            activity VARCHAR(100) NOT NULL,
            category VARCHAR(50) NOT NULL,
            deadline DATETIME,
            completed BOOLEAN NOT NULL,
            FOREIGN KEY (username, category) REFERENCES categories(username,category) ON DELETE CASCADE ON UPDATE CASCADE,
            PRIMARY KEY (id_activity) 
        );
    ''')
    conn.commit()

  @staticmethod
  def createUser(username):
    try:
      conn.execute('''
        INSERT INTO users (username) VALUES (?);
      ''', (username,))
      conn.commit()
      return True
    except sqlite3.IntegrityError as e:
        print(e)
        return False

  @staticmethod
  def insertItem(username, activity ,category, deadline=None):
    try:
      m = hashlib.sha256()
      m.update(str(username).encode())
      m.update(str(activity).encode())
      m.update(str(category).encode())
      m.update(str(deadline).encode())
      m.digest()
      id_activity = m.hexdigest()

      conn.execute('''
      INSERT INTO activities (id_activity,username, activity, category,deadline,completed) VALUES (?, ?, ?, ?,?,?);
    ''', (id_activity,username, activity ,category,deadline,False))
      conn.commit()
      return True
    except sqlite3.IntegrityError as e :
      return False

  @staticmethod
  def selectItems(username, category=None):
    if category == None:
      cur.execute('''
      SELECT activity,category,deadline FROM activities WHERE username == (?);
      ''',(username,))
    else:
      cur.execute('''
      SELECT activity,category,deadline FROM activities WHERE username == ? AND category == ?;
      ''',(username,category))

    rows = cur.fetchall()

    return str(rows).strip('[]') if len(rows) > 0 else "No activity found"

  @staticmethod
  def deleteItem(username, activity ,category,deadline):
    
    cur.execute('''
      SELECT * FROM activities WHERE username == ? AND activity == ? AND category == ? AND deadline == ?
    ''', (username, activity ,category,deadline))

    if(len(cur.fetchall()) > 0 ):
      conn.execute('''
        DELETE FROM activities WHERE username == ? AND activity == ? AND category == ? AND deadline == ?
      ''', (username, activity ,category,deadline))
      conn.commit()
      return True
    else:
      return False

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

    cur.execute('''
    SELECT * FROM categories WHERE username == (?);
    ''',(username,)) 

    rows = cur.fetchall()
    if len(rows) > 0:
      categiories_list = ""
      for category in rows:
        if category is not None:
          categiories_list +=  str(category[1]) + ", "
      categiories_list = categiories_list[:-2]
    else:
      categiories_list = "No activity found"

    return categiories_list

  @staticmethod
  def deleteCategory(username, category):

    cur.execute('''
      SELECT * FROM categories WHERE username == ? AND category == ? 
    ''', (username, category))
    
    if(len(cur.fetchall()) > 0 ):
      conn.execute('''
      DELETE FROM categories WHERE username == ? AND category == ? 
    ''', (username, category))
      conn.commit()
      return True
    else:
      return False

  @staticmethod
  def setItemStatus(username, activity ,category,deadline,completed):
    
    cur.execute('''
      SELECT * FROM activities WHERE username == ? AND activity == ? AND category == ? AND deadline == ?
    ''', (username, activity ,category,deadline))
    
    if(len(cur.fetchall()) > 0 ):
      conn.execute('''UPDATE activities SET completed = ? WHERE username == ? AND activity == ? AND category == ? AND deadline == ?
      ''', (completed, username, activity ,category,deadline))
      conn.commit()
      return True
    else:
      return False

  @staticmethod
  def modifyCategory(username, category, category_new):
    cur.execute('''
      SELECT * FROM categories WHERE username == ? AND category == ?
    ''', (username, category))
    if(len(cur.fetchall()) > 0 ):
      conn.execute('''
        UPDATE categories SET category = ? WHERE username == ? AND category == ?;
      ''', (category_new,username,category))
      conn.commit()
      return True
    else:
      return False

  @staticmethod
  def modifyActivity(username, category, activity, deadline, newdeadline = None, newcategory = None, newactivity = None):
    try:
      conn.execute('''
        SELECT * FROM activities WHERE username == ? AND activity == ? AND category == ? AND deadline == ?
      ''', (username, activity , category, deadline))
      if(len(cur.fetchall()) > 0 ):
        if (newdeadline == None and newcategory != None and newactivity == None):
          conn.execute('''UPDATE activities SET category = ? WHERE username == ? AND activity == ? AND category == ? AND deadline == ?
          ''', (newcategory, username, activity , category, deadline))
        elif (newdeadline != None and newcategory == None and newactivity == None):
          conn.execute('''UPDATE activities SET deadline = ? WHERE username == ? AND activity == ? AND category == ? AND deadline == ?
          ''', (newdeadline, username, activity , category, deadline))
        elif (newdeadline == None and newcategory == None and newactivity != None):
          conn.execute('''UPDATE activities SET activity = ? WHERE username == ? AND activity == ? AND category == ? AND deadline == ?
          ''', (newactivity, username, activity , category, deadline))
        elif (newdeadline == None and newcategory != None and newactivity != None):
          conn.execute('''UPDATE activities SET activity = ?, category = ? WHERE username == ? AND activity == ? AND category == ? AND deadline == ?
          ''', (newactivity, newcategory, username, activity , category, deadline))
        elif (newdeadline != None and newcategory == None and newactivity != None):
          conn.execute('''UPDATE activities SET activity = ?, deadline = ? WHERE username == ? AND activity == ? AND category == ? AND deadline == ?
          ''', (newactivity, newdeadline, username, activity , category, deadline))
        elif (newdeadline != None and newcategory != None and newactivity == None):
          conn.execute('''UPDATE activities SET deadline = ?, category = ? WHERE username == ? AND activity == ? AND category == ? AND deadline == ?
          ''', (newdeadline, newcategory, username, activity , category, deadline))
        conn.commit()
        return True
      else:
        return False
    except sqlite3.IntegrityError:
      return False


  @staticmethod
  def doesUserExists(username):
    cur.execute('''
      SELECT * FROM users WHERE username == ?
    ''', (username, ))
    if(len( cur.fetchall()) > 0 ):
      return True
    return False

  @staticmethod
  def doesCategoryExists(username,category):
    cur.execute('''
      SELECT * FROM categories WHERE username == ? AND category == ?
    ''', (username, category))
    if(len( cur.fetchall()) > 0 ):
      return True
    return False