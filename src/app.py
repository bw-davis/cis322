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
        return render_template('create_user.html')
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        conn =  psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
        cur = conn.cursor()
        if role == 'Facilities Officer' or role == 'Logistics Officer':
            cur.execute("insert into users values (%s, %s, %s);", (username, password, role))
        else:
            cur.execute("insert into users values (%s, %s);", (username, password))
        conn.commit()
        cur.close()
        conn.close()
        return render_template('dashboard.html', username=username)
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
        rows = cur.fetchone()[0]
        if rows != 1:
            error = "Username and Password do not match. Please try again."
            cur.close()
            conn.close()
        else:
            return render_template('dashboard.html', username=username)
    return render_template('login.html', error=error)

@app.route("/dashboard", methods=('GET', ))
def dashboard():
    return render_template('dashboard.html')

@app.route("/add_facility", methods=('GET', 'POST'))
def add_facility():
    error = None
    if request.method=='GET':
        return render_template('add_facility.html')
    if request.method=='POST':
        name = request.form['name']
        code = request.form['code']
        conn =  psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
        cur = conn.cursor()
        cur.execute("insert into facilities (name, code) values (%s, %s);", (name, code))
        error = "facility added successfully"
        conn.commit()
        cur.close()
        conn.close()
    return render_template('add_facility.html', error=error)

@app.route("/add_asset", methods=('GET', 'POST'))
def add_asset():
    error = None
    if request.method=='GET':
        return render_template('add_asset.html')
    if request.method=='POST':
        tag = request.form['tag']
        description = request.form['description']
        conn =  psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
        cur = conn.cursor()
        cur.execute("insert into assets (asset_tag, description) values (%s, %s);", (tag, description))
        error = "asset added successfully"
        conn.commit()
        cur.close()
        conn.close()
    return render_template('add_asset.html', error=error)
 
if __name__ == "__main__":
    app.run()
