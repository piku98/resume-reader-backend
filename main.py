from flask import Flask, request, jsonify, send_from_directory, send_file, make_response
from flask_cors import CORS
import sqlite3
from controllers.dbops import make_all_tables
from werkzeug.datastructures import FileStorage
from controllers.dbops import get_last_row_id
from controllers.dbops import get_details
from controllers.dbops import downloadDB
from controllers.dbops import updateRow
import io
import os

app = Flask(__name__)
cors = CORS(app)


conn = sqlite3.connect('database.db', check_same_thread=False)
cur = conn.cursor()
make_all_tables(conn)

from utilities.collectalldata import collect_details
from controllers.acceptfile import accept_file



@app.route('/', methods=['GET', 'POST'])
def hello():
    return 'hello'

@app.route('/fileupload', methods=['POST'])
def fileupload():
    if 'file' not in request.files and not request.files['file']:
        resp = jsonify({"success": False, "message": "no file present."})
        resp.status_code = 400
        return resp
    
    file1 = request.files["file"]
    #file2 = request.files.getlist("file")[1]

    filename = file1.filename
    i = len(filename) - 1
    while filename[i] != '.':
        i -= 1
    extension = filename[i + 1:]
    #print(extension)
    if extension == 'docx' or extension == 'pdf':
        #file2.save(get_last_row_id(cur) + '.' + extension)
        details = accept_file(file1, extension, cur, conn)
        print(details)
        if not details:
            resp = jsonify({"success": False, "message": "Person in resume already stored in db"})
            resp.status_code = 400
            return resp
        resp = jsonify({"success": True, "message": details}) 
        resp.status_code = 200
        return resp
        
    else:
        resp = jsonify({"success": False, "message": "only pdf and docx file extensions are supported."})
        resp.status_code = 400
        return resp 


@app.route('/getdetails', methods=['GET'])
def getPersonDetails():
    key = request.args.get('key')
    val = request.args.get('val')
    
    if not key and not val:
        resp = jsonify({"success": False, "message": "key and val missing"})
        resp.status_code = 400
        return resp
    
    dic = get_details([key, val], cur)

    resp = jsonify({"success": True, "message": dic})  
    resp.status_code = 200
    return resp  


@app.route('/downloadfile', methods=['GET'])
def downloadfile():
    id = request.args.get("id")
    
    if not id:
        resp = jsonify({"success": False, "message": "id missing"})
        resp.status_code = 400
        return resp


    for root, dirs, files in os.walk('./project/backend/file_data/resume_files/'):
        for f in files:
            i = len(f) - 1
            while f[i] != '.':
                i -= 1
            name = f[0:i]
            print(f)
            if str(id) == name:
                return send_file('file_data/resume_files/' + f, as_attachment=True, attachment_filename=f, mimetype='application/docx')

    resp = jsonify({"success": False, "message": "Not found"})
    resp.status_code = 404
    return resp


@app.route("/downloaddb", methods=['GET'])
def downloaddb():
    si = downloadDB(cur)
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=DB.csv"
    output.headers["Content-type"] = "text/csv"
    return output

@app.route("/updateinfo", methods=['POST'])
def updateinfo():
    data = request.get_json()
    if not data:
        resp = jsonify({"success": False, "message": "No data"})
        resp.status_code = 400
        return resp
    
    updateRow(cur, data)
    conn.commit()
    
    resp = jsonify({"success": True, "message": "Successfully updated"})
    resp.status_code = 200
    return resp
    





if __name__ == '__main__':
      app.run(host='localhost', port=5000)
