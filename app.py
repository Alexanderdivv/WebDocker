from flask import Flask, render_template, url_for, request
import os
import mysql.connector
from werkzeug.utils import secure_filename
import socket
from datetime import datetime
import pytz
import base64


app = Flask(__name__)

# @app.route("/")
# def index():
#     time_zone = pytz.timezone("Asia/Jakarta")
#     current_time = datetime.now(time_zone).strftime("%Y-%m-%d %H:%M:%S")
#     return f"Hostname: {socket.gethostname()}<br>Current Time in Indonesia: {current_time}"    

# convert image to binary to store in database (blob)
def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData


db = mysql.connector.connect(
    host='db-uploadimage.ctnvddv68d9z.ap-northeast-3.rds.amazonaws.com',
    user='admin',
    password='12341234',
    database='webimage'
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
    cursor.execute('SELECT * FROM tableimg')
    results = cursor.fetchall()
    return render_template("index.html", results=results)

# @app.route('/', methods = ['GET', 'POST'])
# def upload_file():
#    if request.method == 'POST':
#       f = request.files['file']
#       f.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(f.filename)))
#       return 'file uploaded successfully'


# upload nama ke database
@app.route('/', methods=['POST', 'GET'])
def upload():
    file = request.files['file']
    name = request.form['name']
    #save image to local directory (efsdata)
    file.save(os.path.join("/efsdata", secure_filename(file.filename)))

    # get the path of the image
    path = os.path.join("/efsdata", secure_filename(file.filename))

    sql = "INSERT INTO tableimg (image, name) VALUES (%s, %s)"
    val = (name, path)
    # sql = "INSERT INTO webimg (name) VALUES (%s)"
    # val = (name,)
    cursor = db.cursor()
    cursor.execute(sql, val)
    db.commit()
    return render_template("index.html")

    #         # get the file from the form and convert it to binary, then save it to the database

    #     file = request.files['file']
    #     name = request.form['name']
    #     #save image to local directory (efsdata)
    #     file.save(os.path.join("efsdata", secure_filename(file.filename))) not working

    #     # get the path of the image
    #     path = os.path.join("efsdata", secure_filename(file.filename))


    #     # save the directory of the image to the database
    #     # image = file.save(os.path.join("efsdata", secure_filename(file.filename)))      
    #     sql = "INSERT INTO tableimg (image, name) VALUES (%s, %s)"
    #     val = (name, path)
    #     # sql = "INSERT INTO webimg (name) VALUES (%s)"
    #     # val = (name,)
    #     cursor = db.cursor()
    #     cursor.execute(sql, val)
    #     db.commit()
    #     # return "Upload Success"
    #     return render_template("index.html")
    
    # return "Upload Failed"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)