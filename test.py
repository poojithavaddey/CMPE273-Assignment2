import sqlite3, json
from flask import jsonify

conn = sqlite3.connect('my_db.db',check_same_thread=False)
c= conn.cursor()


def create_table():
    c.execute('''CREATE TABLE if not exists tests(
    test_id integer PRIMARY KEY AUTOINCREMENT,
    subject text not null,
    answer_keys text not null)
     ''')
    print("Created Tests Table")

    c.execute('''CREATE TABLE if not exists scantrons(
    scantron_id integer PRIMARY KEY AUTOINCREMENT,
    test_id integer,
    name text not null,
    subject text not null,
    submissions text)
     ''')
    print("Created Scantron Table")
    conn.commit()

def insert_into_tests(entities):
    print(entities[0], "::::", json.dumps(entities[1]))
    c.execute('INSERT INTO tests(subject,answer_keys) values(?,?)',(entities[0],json.dumps(entities[1])))
    print("Inserted into Tests")
    c.execute('Select scantron_id from scantrons order by scantron_id DESC LIMIT 1')
    conn.commit()
    

def insert_into_scantrons(t_id,entries):
    c.execute("INSERT INTO scantrons(test_id,name,subject,submissions) values('%s', '%s','%s','%s')"%(t_id,entries[0],entries[1],json.dumps(entries[2])))
    print("Inserted into Scantrons") 
    c.execute('Select scantron_id from scantrons order by scantron_id DESC LIMIT 1')
    s_id = c.fetchall()
    conn.commit()  
    return s_id[0]

def get_answer_key(id):
    c.execute('select answer_keys from tests where test_id ='+id)
    row = c.fetchall()
    return row

def get_data():
    c.execute('''select * from tests t left join scantrons s on t.test_id= s.test_id order by test_id DESC LIMIT 1''')
    rows = c.fetchall()
    return rows


def get_sub_data(t_id):
    c.execute('''select * from tests t left join scantrons s on t.test_id= s.test_id where t.test_id='%s'; '''%(t_id))
    row = c.fetchall()
    print( row)
    return row