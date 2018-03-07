from flask import Flask, Response, request
import pymongo

DB_NAME = 'iotree'
DB_HOST = 'ds229435.mlab.com'
DB_PORT = 23
DB_USER = 'steve'
DB_PASS = '123456'

connection = pymongo.MongoClient(DB_HOST, DB_PORT)
db =  connection[DB_NAME]
db.authenticate(DB_USER, DB_PASS)

app = Flask(__name__)

@app.route('/')
def from_field():
    field_data = db['field_data']
    field_data.insert(request.form)
    return 'success'

#FLASK_APP=app.py flask run --host 0.0.0.0

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
