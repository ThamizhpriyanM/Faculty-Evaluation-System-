from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import mysql.connector
from io import BytesIO
import pandas as pd
import os
from flask import flash
import matplotlib.pyplot as plt
import random

app = Flask(__name__)

app.secret_key = 'xyzsdfg'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'project'
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="project"
)
mycursor = mydb.cursor()
mysql = MySQL(app)

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'userType' in request.form:
        username = request.form['username']
        password = request.form['password']
        userType = request.form['userType']

        cursor = mysql.connection.cursor()
        if userType == 'student':
            cursor.execute('SELECT * FROM log WHERE username = %s AND password = %s', (username, password))
        elif userType == 'faculty':
            cursor.execute('SELECT * FROM flog WHERE username = %s AND password = %s', (username, password))
        elif userType == 'admin':
            cursor.execute('SELECT * FROM alog WHERE username = %s AND password = %s', (username, password))
        
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account[0]
            session['username'] = account[1]
            if userType == 'student':
                app.logger.info('Redirecting to student page')
                return redirect(url_for('student'))
            elif userType == 'faculty':
                app.logger.info('Redirecting to faculty page')
                return redirect(url_for('faculty'))
            elif userType == 'admin':
                app.logger.info('Redirecting to admin page')
                return redirect(url_for('admin'))
        else:
            msg = 'Incorrect username/password!'
            app.logger.error(msg)
            return render_template('login.html', msg=msg)

    return render_template('login.html')

@app.route('/student')
def student():
    if 'loggedin' in session:
        app.logger.info('Rendering student.html')
        return render_template('student.html', username=session['username'])
    app.logger.error('User not logged in. Redirecting to login page')
    return redirect(url_for('login'))

@app.route('/faculty')
def faculty():
    if 'loggedin' in session:
        app.logger.info('Rendering faculty.html')
        return render_template('faculty.html', username=session['username'])
    app.logger.error('User not logged in. Redirecting to login page')
    return redirect(url_for('login'))

@app.route('/admin')
def admin():
    if 'loggedin' in session:
        app.logger.info('Rendering admin.html')
        return render_template('admin.html', username=session['username'])
    app.logger.error('User not logged in. Redirecting to login page')
    return redirect(url_for('login'))

@app.route('/new')
def new():
    return render_template('new2.html')

from flask import session

@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        column1 = request.form['faculty_name']
        column2 = request.form['two']
        column3 = request.form['three']
        column4 = request.form['four']
        column5 = request.form['five']
        column6 = request.form['six']
        column7 = request.form['seven']
        column8 = request.form['eight']
        column9 = request.form['nine']
        
        
        if 'username' in session:
            username = session['username']
        else:
            username = None
        
       
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO analize (column1, column2, column3, column4, column5, column6, column7, column8, column9, username) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                       (column1, column2, column3, column4, column5, column6, column7, column8, column9, username))
        mysql.connection.commit()
        cursor.close()
        flash('Data uploaded successfully!', 'success')
        return redirect(url_for('form'))
    else:
        return render_template('form.html')


    



@app.route('/generate_graph')
def generate_graph():
    avg_values = {
        'Teaching': round(random.uniform(5, 10), 1),
        'Lectures': round(random.uniform(5, 10), 1),
        'Communication': round(random.uniform(5, 10), 1),
        'Discussion and Clarification': round(random.uniform(5, 10), 1),
        'Classroom Management': round(random.uniform(5, 10), 1),
        'Academic Progress': round(random.uniform(5, 10), 1),
        'Teaching Methods': round(random.uniform(5, 10), 1),
        'Overall Performance': round(random.uniform(5, 10), 1)
    }
    return render_template('graph.html', avg_values=avg_values)




@app.route('/display_data', methods=['POST'])
def display_data():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM analize")
    data = cursor.fetchall()
    cursor.close()
    return render_template('response.html', data=data)


@app.route('/search', methods=['POST'])
def search():
    search_value = request.form['search_value']
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM analize WHERE username = %s", (search_value,))
    data = cursor.fetchall()
    cursor.close()
    return render_template('response.html', data=data)

@app.route('/fsearch', methods=['POST'])
def fsearch():
    search_value = request.form['search_value']
    cursor = mysql.connection.cursor()
    cursor.execute("""
    SELECT
        AVG(column2) AS avg_column2,
        AVG(column3) AS avg_column3,
        AVG(column4) AS avg_column4,
        AVG(column5) AS avg_column5,
        AVG(column6) AS avg_column6,
        AVG(column7) AS avg_column7,
        AVG(column8) AS avg_column8,
        AVG(column9) AS avg_column9
    FROM
        analize
    WHERE   
        column1 = %s 
    GROUP BY
        column1;
""", (search_value,))
   
    data = cursor.fetchall()
    cursor.close()
    return render_template('search.html', data=data)


@app.route('/particular')
def particular():
    return render_template('particular_response.html')

@app.route('/fac')
def fac():
    return render_template('fac.html')
    
@app.route('/login')
def login1():
    app.logger.info('Rendering login.html')
    return render_template('login.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/course')
def course():
    return render_template('course.html')


if __name__ == "__main__":
    # Set up logging
    import logging
    logging.basicConfig(level=logging.DEBUG)
    app.run(debug=True)
