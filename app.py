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

db = mysql.connector.connect(
    host='db-uploadimage.ctnvddv68d9z.ap-northeast-3.rds.amazonaws.com',
    user='admin',
    password='12341234',
    database='webimg'
)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/db')
def getDB():
    cursor = db.cursor()
    cursor.execute('SELECT * FROM your_table')
    results = cursor.fetchall()
    return str(results)

@app.route('/', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(f.filename)))
      return 'file uploaded successfully'
   

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)