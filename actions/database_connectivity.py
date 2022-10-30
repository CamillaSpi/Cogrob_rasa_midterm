import sqlite3

conn = sqlite3.connect('data.db')

print("connected")

class Database:

  @staticmethod
  def initDb():
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
            FOREIGN KEY (username) REFERENCES users(username)
        );
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS activities (
            username VARCHAR(100) NOT NULL,
            activity VARCHAR(100) NOT NULL,
            category VARCHAR(50) NOT NULL,
            deadline TIME(0) NOT NULL,
            completed BOOLEAN NOT NULL,
            FOREIGN KEY (username) REFERENCES users(username),
            FOREIGN KEY (category) REFERENCES categories()
        );
    ''')
    conn.commit()

  
  @staticmethod
  def insert(name, emp_code, email):
    conn.execute('''
      INSERT INTO candidates (NAME, EMPLOYEE_CODE, EMAIL) VALUES (?, ?, ?);
    ''', (name, emp_code, email))
    conn.commit()


  @staticmethod
  def select():

    cur = conn.cursor()

    cur.execute('''
      SELECT * FROM candidates;
    ''')

    rows = cur.fetchall()

    return str(rows).strip('[]') if len(rows) > 0 else "No records found"

  @staticmethod
  def delete(value):

    name = value + "%"

    conn.execute('''
      DELETE FROM candidates WHERE name like ? OR employee_code like ?
    ''', (name, value,))
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