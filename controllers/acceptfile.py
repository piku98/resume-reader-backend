import os
os.chdir('..')
from utilities.collectalldata import collect_details
from controllers.dbops import insert_into_resume_details

def accept_file(file1, extension, curr, conn):
    
    details = collect_details(file1, extension)
    try:
        lastrowid = insert_into_resume_details(details, curr)
        details['id'] = lastrowid
        conn.commit()
    except:
        details = None
    return details