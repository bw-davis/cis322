from flask import Flask, flash, redirect, render_template, request, session, abort
import json
import os
import pathlib
import psycopg2
from configure import dbname, dbhost, dbport

app = Flask(__name__)

@app.route("/create_user", methods=('POST', 'GET',))
def create_user():
    error = None
    if request.method == 'GET':
        return render_template('create_user.html')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
        cur = conn.cursor
        cur.execute("SELECT * from users where user_pk=%s", (username, ))
        row = cur.fetchall()
        if row:
            error = 'Username is already taken.  Please try another'
        else:
            cur.execute("INSERT into users VALUES (%s, %s)", (username, password, ))  
        conn.commit()
        cur.close()
        conn.close()
        return render_template('dashboard.html', data='username')
    return render_template('login.html', error=error)

@app.route("/")
@app.route("/login", methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
        cur = conn.cursor
        cur.execute("SELECT password from users where user_pk=%s", (username, ))
        rows = cur.fetchall()
        for row in rows:
            if row:
                if row == password:
                    return render_template('dashboard.html', data='username')
            else:
                error = 'Username and Password do not match.  Please try again.' 
        conn.commit()
        cur.close()
        conn.close()
    return render_template('login.html', error=error)

@app.route("/dashboard")
def dashboard():
    return render_template('dashboard.html')
 
if __name__ == "__main__":
    app.run()
