from flask import Flask, flash, redirect, render_template, request, session, abort
import json
import os
import pathlib
import psycopg2
from configure import dbname, dbhost, dbport

app = Flask(__name__)

@app.route("/create_user", methods=('GET', 'POST'))
def create_user():
    error = None
    if request.method=='GET':
        print("hey brian")
        return render_template('create_user.html')
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        conn =  psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
        cur = conn.cursor()
            #cur.execute("select * from users where user_pk=%s;", (username))
            #row = cur.fetchall()
            # if row:
            #     print(row)
            #     error = 'Username is already taken.  Please try another'
            # else:
        cur.execute("insert into users values (%s, %s);", (username, password))
        conn.commit()
        cur.close()
        conn.close()
        return render_template('dashboard.html')
    return render_template('login.html', error=error)

@app.route("/")
@app.route("/login", methods=('GET', 'POST'))
def login():
    if request.method=='GET':
        return render_template('login.html')
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        conn = psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
        cur = conn.cursor()
        cur.execute("select count(*) from users where user_pk=%s and password=%s;", (username, password))
        #cur.execute("select (count)* from users where user_pk=%s and password=%s;", (username, password))
        rows = cur.fetchone()[0]
        if rows != 1:
            error = "Username and Password do not match. Please try again."
        # for row in rows:
        #     if row == password:
        #         return render_template('dashboard.html')
        #     else:
        #         error = 'Username and Password do not match.  Please try again.'
            cur.close()
            conn.close()
        else:
            return render_template('dashboard.html', username=username)
    return render_template('login.html', error=error)

@app.route("/dashboard", methods=('GET', ))
def dashboard():
    return render_template('dashboard.html')
 
if __name__ == "__main__":
    app.run()
