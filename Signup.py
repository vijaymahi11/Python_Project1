from operator import attrgetter
from flask import Flask
from tkinter import *
from tkinter import messagebox
from flask_cors import CORS, cross_origin
from flask import Flask, flash, render_template, request, redirect, url_for, session, send_file
from flask_mysqldb import MySQL
from flaskext.mysql import MySQL
from flask import jsonify, send_file
from werkzeug.utils import secure_filename
import pymysql
import re
import os
import calendar
import math
from datetime import datetime
from flask import Flask
from flask_mail import Mail, Message
app = Flask(__name__)
UPLOAD_FOLDER = '/Users/Tigma User/demo/src/images/'
cors = CORS(app, resources={r'*': {'origins': '*'}})
app.config['UPLOAD_FOLDER'] = '/Users/Tigma User/demo/src/images/'
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'vijayMahi'
app.config['MYSQL_DATABASE_DB'] = 'emp_register'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql = MySQL(app)
mysql.init_app(app)

@app.route('/data', methods=['POST', 'GET'])
def register():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':
        data = request.json
        print(data)
        email = data['values']['email']
        str1 = f"""SELECT * FROM employee_data where email='{data['values']['email']}';"""
        cur.execute(str1)
        account = cur.fetchone()
        if account:
            return jsonify({'status': 400, 'msg': 'enter valid email'})
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            return jsonify({'status': 200, 'msg': 'Invalid email address !'})
        else:
            cur.execute(
                f"""INSERT INTO employee_data(firstname,lastname,email,mobileno,country,city,password,gender,profile) VALUES('{data['values']['firstname']}','{data['values']['lastname']}','{data['values']['email']}','{data['values']['mobileno']}','{data['values']['country']}','{data['values']['city']}','{data['values']['password']}','{data['values']['gender']}','/Users/Tigma User/demo/src/images/{data['values']['profile']}'); """)
            conn.commit()
            return jsonify({'status': 200, 'msg': 'Successfully Register!'})
