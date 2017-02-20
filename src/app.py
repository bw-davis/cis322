from flask import Flask, flash, redirect, render_template, request, session, abort
import json
import os
import pathlib
import psycopg2

app = Flask(__name__)
global dbhost, dbname, dbport

@app.route("/create_user", methods=['POST', 'GET'])
def create_user():
    error = None
    if request.method == 'GET':
        return render_template('create_user.html')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = psycopg2.connect("dbname=%(dbname)s host=%(dbhost)s port=%(dbport)s")
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
    return render_template('create_user.html', error=error)

 
if __name__ == "__main__":
    cpath = pathlib.Path(os.path.realpath(__file__)).parent.joinpath('lost_config.json')
    with cpath.open() as conf:
        c = json.load(conf)
        dbhost = c['database']['dbhost']
        dbport = c['database']['dbport']
        dbname = c['database']['dbname']
    app.run()