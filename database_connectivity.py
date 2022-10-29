import sqlite3

def DataUpdate(facility_type,location):
    conn = sqlite3.connect('data.db')

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

if __name__=="__main__":
    DataUpdate("hospital","San Francisco")
