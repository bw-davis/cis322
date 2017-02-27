from flask import Flask, flash, redirect, render_template, request, session, abort
import json
import os
import pathlib
import psycopg2
from configure import dbname, dbhost, dbport

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

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
        if role == 'Facilities Officer':
            cur.execute("insert into users values (%s, %s, 2);", (username, password))
            session['role'] = 'Facilities Officer'
        elif role == 'Logistics Officer':
            cur.execute("insert into users values (%s, %s, 1);", (username, password))
            session['role'] = 'Logistics Officer'
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
            session['username'] = username
            session['password'] = password
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
        good = "facility added successfully"
        conn.commit()
        cur.close()
        conn.close()
        return render_template('add_facility.html', good=good)
    return render_template('add_facility.html', error=error)

@app.route("/add_asset", methods=('GET', 'POST'))
def add_asset():
    error = None
    if request.method=='GET':
        conn =  psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
        cur = conn.cursor()
        cur.execute("select code from facilities;")
        facilities = cur.fetchall()
        return render_template('add_asset.html', facilities=facilities)
    if request.method=='POST':
        tag = request.form['tag']
        description = request.form['description']
        facility_code = request.form['facility_code']
        conn =  psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
        cur = conn.cursor()
        cur.execute("select count(*) from assets where asset_tag=%s;", (tag))
        count = cur.fetchone()[0]
        if count != 1:
            cur.execute("insert into assets (asset_tag, description) values (%s, %s);", (tag, description))
            cur.execute("insert into asset_at (asset_fk, facility_fk) select asset_pk, facility_pk from assets a, facilities f where a.asset_tag=%s and f.code=%s;", (tag, facility_code))
            good = "asset added successfully"
            conn.commit()
        else:
            error = "duplicate asset"
            return render_template('add_asset.html', error=error)
        cur.close()
        conn.close()
        return render_template('add_asset.html', good=good)
    return render_template('add_asset.html', error=error)

@app.route("/dispose_asset", methods=('GET', 'POST'))
def dispose_asset():
    error = None
    # if session['role'] != 'Logistics Officer':
    #     error = 'only Logistics Officers can dispose of assets'
    #     return render_template('dispose_asset.html', error=error)
    if request.method=='GET':
        conn =  psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
        cur = conn.cursor()
        cur.execute("select asset_tag from assets;")
        assets = cur.fetchall()
        return render_template('dispose_asset.html', assets=assets)
    if request.method=='POST':
        asset_tag = request.form['asset_tag']
        conn =  psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
        cur = conn.cursor()
        cur.execute("delete from assets where asset_tag=%s", (asset_tag))
        good = "asset deleted"
        conn.commit()
        cur.close()
        conn.close()
        return render_template('dispose_asset.html', good=good)
    return render_template('dispose_asset.html', error=error)
 
if __name__ == "__main__":
    app.run()
