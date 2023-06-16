from flask import Flask, render_template, url_for, request
import os
import mysql.connector
from werkzeug.utils import secure_filename
import socket
from datetime import datetime
import pytz

app = Flask(__name__)

# @app.route("/")
# def index():
#     time_zone = pytz.timezone("Asia/Jakarta")
#     current_time = datetime.now(time_zone).strftime("%Y-%m-%d %H:%M:%S")
#     return f"Hostname: {socket.gethostname()}<br>Current Time in Indonesia: {current_time}"    

# convert image to binary to store in database (blob)
def convertToBinary(filename):
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData


db = mysql.connector.connect(
    host='db-uploadimage.ctnvddv68d9z.ap-northeast-3.rds.amazonaws.com',
    user='admin',
    password='12341234',
    database='webimg'
)

# @app.route("/")
# def index():
#     return render_template("index.html")

# @app.route('/db')
# def getDB():
#     cursor = db.cursor()
#     cursor.execute('SELECT * FROM webimg')
#     results = cursor.fetchall()
#     return str(results)

# show all data from database in the table form (index.html)
@app.route('/')
def getDB():
    cursor = db.cursor()
    cursor.execute('SELECT * FROM webimg')
    results = cursor.fetchall()
    return render_template("index.html", results=results)

# @app.route('/', methods = ['GET', 'POST'])
# def upload_file():
#    if request.method == 'POST':
#       f = request.files['file']
#       f.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(f.filename)))
#       return 'file uploaded successfully'

# store filename and image as binary to database (blob), id is auto increment
# @app.route('/upload', methods=['POST'])
# def upload():
#     cursor = db.cursor()
#     if request.method == 'POST':
#         file = request.files['file']
#         filename = secure_filename(file.filename)
#         file.save(os.path.join('static/images', filename))
#         sql = "INSERT INTO webimg (filename, image) VALUES (%s, %s)"
#         val = (filename, convertToBinary(os.path.join('static/images', filename)))
#         cursor.execute(sql, val)
#         db.commit()
#         return "Upload Success"
    
#     return "Upload Failed"


# upload only filename field received from form to database
@app.route('/upload', methods=['POST', 'GET'])
def upload():
    cursor = db.cursor()
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        sql = "INSERT INTO webimg (filename) VALUES (%s)"
        val = (filename,)
        cursor.execute(sql, val)
        db.commit()
        return "Upload Success"
    
    return "Upload Failed" 

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)