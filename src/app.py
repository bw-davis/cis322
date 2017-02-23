from flask import Flask, flash, redirect, render_template, request, session, abort
import json
import os
import pathlib
import psycopg2

app = Flask(__name__)
global dbhost, dbname, dbport

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
        cur.execute("SELECT * from users where user_pk=%(username)s")
        row = cur.fetchall()
        if row:
            error = 'Username is already taken.  Please try another'
        else:
            cur.execute("INSERT into users VALUES (%(username)s, %(password)s")  
        conn.commit()
        cur.close()
        conn.close()
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
        cur.execute("SELECT password from users where user_pk=%(username)s")
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
 
if __name__ == "__main__":
    cpath = pathlib.Path(os.path.realpath(__file__)).parent.joinpath('lost_config.json')
    with cpath.open() as conf:
        c = json.load(conf)
        dbhost = c['database']['dbhost']
        dbport = c['database']['dbport']
        dbname = c['database']['dbname']
    app.run()