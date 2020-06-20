import sqlite3
import csv
import io

def resume_details(conn):
    conn.execute('''CREATE TABLE IF NOT EXISTS resume_details
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    phone TEXT NOT NULL UNIQUE,
    linkedin TEXT NOT NULL UNIQUE,
    fonts TEXT NOT NULL,
    tables INTEGER NOT NULL,
    images INTEGER NOT NULL);''')

def make_all_tables(conn):
    resume_details(conn)


def insert_into_resume_details(details, curr):
    curr.execute('''INSERT INTO resume_details VALUES(?,?,?,?,?,?,?,?)
    ''',[None, details['name'], details['email'], details['phone'], details['linkedin'], str(details['fonts']), details['n_tables'], details['n_images']])
    
    return curr.lastrowid


def get_last_row_id(curr):
    curr.execute('''SELECT MAX(id) FROM resume_details''')
    return str(curr.fetchone()[0])


def get_details(parameter, curr):
    curr.execute('''SELECT * FROM resume_details;''')
    rows = curr.fetchall()
    search_params = ["id", "name", "email", "phone", "linkedin", "fonts", "tables", "images"]
    dicts = []
    for row in rows:
        d = {}
        for i in range(len(search_params)):
            d[search_params[i]] = row[i]
            dicts.append(d)
    ret = []
    for dic in dicts:
        if parameter[1] in dic[parameter[0]]:
            ret.append(dic)
    
    return ret


def downloadDB(curr):
    curr.execute('''SELECT * FROM resume_details''')
    rows = curr.fetchall()
    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow(("id", "name", "email", "phone", "linkedin", "fonts", "table", "images"))
    cw.writerows(rows)
    return si
    
def updateRow(curr, details):
    curr.execute('''UPDATE resume_details 
    SET name=?, email=?, phone=?, linkedin=?, fonts=?, tables=?, images=?
    WHERE id=?
    ''', [details['name'], details['email'], details['phone'], details['linkedin'], details['fonts'], details['tables'], details['images'], details['id']])


