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
            reminder BOOLEAN NOT NULL,
            FOREIGN KEY (username, category) REFERENCES categories(username,category) ON DELETE CASCADE ON UPDATE CASCADE,
            PRIMARY KEY (id_activity) 
        );
    ''')
    conn.commit()

  @staticmethod
  def doesCategoryExists(username,category):
    cur.execute('''
      SELECT * FROM categories WHERE username == ? AND category == ?
    ''', (username, category))
    if(len( cur.fetchall()) > 0 ):
      return True
    return False

  @staticmethod
  def doesActivityExists(username,category,activity,deadline=None):
    cur.execute('''
      SELECT * FROM activities WHERE username == ? AND category == ? AND activity == ? AND deadline == ?
    ''', (username, category, activity, deadline))
    if(len( cur.fetchall()) > 0 ):
      return True
    return False

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
  def insertItem(username, activity ,category, reminder,deadline=None):
    try:
      m = hashlib.sha256()
      m.update(str(username).encode())
      m.update(str(activity).encode())
      m.update(str(category).encode())
      m.update(str(deadline).encode())
      m.digest()
      id_activity = m.hexdigest()

      conn.execute('''
      INSERT INTO activities (id_activity,username, activity, category,deadline,completed,reminder) VALUES (?, ?, ?, ?,?,?,?);
    ''', (id_activity,username, activity ,category,deadline,False,reminder))
      conn.commit()
      return True
    except sqlite3.IntegrityError as e :
      return False

  @staticmethod
  def selectItems(username, category=None, activity_status=None):
    if(activity_status == "completed"):
      completed = True
    elif(activity_status == "uncompleted"):
      completed = False
    if (category != None and activity_status != None):
      cur.execute('''
      SELECT activity,category,deadline,completed FROM activities WHERE username == ? AND category == ? AND completed == ?;
      ''',(username,category,completed))
    elif category == None and activity_status != None:
      cur.execute('''
      SELECT activity,category,deadline,completed FROM activities WHERE username == ? AND completed == ?;
      ''',(username,completed))
    elif category != None and activity_status == None:
      cur.execute('''
      SELECT activity,category,deadline,completed FROM activities WHERE username == ? AND category == ?;
      ''',(username,category))
    else:  
      cur.execute('''
      SELECT activity,category,deadline,completed FROM activities WHERE username == (?);
      ''',(username,))

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
  def modifyActivity(username, category, activity, deadline, newcategory = None, newactivity = None, newdeadline = None):
    try:
      m = hashlib.sha256()
      m.update(str(username).encode())
      m.update(str(activity).encode())
      m.update(str(category).encode())
      m.update(str(deadline).encode())
      m.digest()
      print(str(username)+str(activity)+str(category)+str(deadline))
      id_activity = m.hexdigest()
      cur.execute('''
        SELECT * FROM activities WHERE id_activity == ?
      ''', (id_activity,))
      if(len(cur.fetchall()) > 0 ):
        
        if newcategory != None:
          if not Database.doesCategoryExists(username,newcategory):
            Database.insertCategory(username, newcategory)
        paramList = list()
        paramList.append(("category", newcategory))
        paramList.append(("activity", newactivity))
        paramList.append(("deadline",newdeadline))
        queryParam=""
        tupleParam = ()
        p = hashlib.sha256()
        for param in paramList:
          if param[1] is not None:
            tupleParam += (param[1],)
            queryParam += ", " + str(param[0]) + " = ?"
          else:
            param = (param[0],exec(param[0]))
          p.update(str(param[1]).encode())
          print(str(param[1]))
        p.digest()
        id_activity_new = p.hexdigest()
        queryParam += ", id_activity = ?"
        tupleParam += (id_activity_new, id_activity,)
        query = "UPDATE activities SET" + queryParam[1:] + " WHERE id_activity == ?"
        print(query)
        print(tupleParam)
        conn.execute(query, tupleParam)
        conn.commit()
        return True
      else:
        return False
    except sqlite3.IntegrityError as e:
      print(e)
      return False


  @staticmethod
  def doesUserExists(username):
    cur.execute('''
      SELECT * FROM users WHERE username == ?
    ''', (username, ))
    if(len( cur.fetchall()) > 0 ):
      return True
    return False

