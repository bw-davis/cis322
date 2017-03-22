from flask import Flask, flash, redirect, render_template, request, session, abort
import json
import os
import pathlib
import psycopg2
from configure import dbname, dbhost, dbport

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

@app.route("/activate_user", methods=('POST', ))
def activate_user():
    error = "Request Wasn't Sent as POST"
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        session['error'] = None
        role = request.form['role']
        conn =  psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
        cur = conn.cursor()
        cur.execute("select count(*) from users where user_pk=%s;", (username, ))
        count = cur.fetchone()[0]
        if count == 1:
            cur.execute("update users set password=%s, active='TRUE' where user_pk=%s;", (password, username, ))
            conn.commit()
            cur.close()
            conn.close()
            return "user's password was updated and their account is now active"
        if role == 'facofc':
            cur.execute("insert into users values (%s, %s, 2);", (username, password))
            session['role'] = 'Facilities Officer'
        elif role == 'logofc':
            cur.execute("insert into users values (%s, %s, 1);", (username, password))
            session['role'] = 'Logistics Officer'
        else:
            error = "Role was neither 'facofc' nor 'logofc'"
            return error
        conn.commit()
        cur.close()
        conn.close()
        return "user added successfully"
    return render_template('error.html', error=error)

@app.route("/revoke_user", methods=('POST', ))
def revoke_user():
    error = "Request Wasn't Sent as POST"
    if request.method=='POST':
        username = request.form['username']
        conn =  psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
        cur = conn.cursor()
        cur.execute("update users set active='FALSE' where user_pk=%s;", (username, ))
        conn.commit()
        cur.close()
        conn.close()
        error = "users account revoked"
        return error
    return error

@app.route("/")
@app.route("/login", methods=('GET', 'POST'))
def login():
    session['error'] = None
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
            cur.execute("select active from users where user_pk=%s;", (username, ))
            active = cur.fetchone()[0]
            if active == False:
                error = "Your account is revoked. Contact sysadmin"
                return error
            session['username'] = username
            session['password'] = password
            cur.execute("select role_fk from users where user_pk=%s;", (username, ))
            role = cur.fetchone()[0]
            if role == 1:
                session['role'] = 'Logistics Officer'
            else:
                session['role'] = 'Facilities Officer'    
            return redirect('dashboard')
    return render_template('login.html', error=error)

@app.route("/dashboard", methods=('GET', ))
def dashboard():
    if session['role'] == 'Logistics Officer':
        logofc = True
        return render_template('dashboard.html', username=session['username'], logofc=logofc, error=session['error'])
    else:
        facofc = True
        return render_template('dashboard.html', username=session['username'], facofc=facofc, error=session['error'])
    return render_template('dashboard.html', username=session['username'])

@app.route("/load_unload", methods=('GET', ))
def load_unload():
    return render_template('load_unload.html')

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
        session['error'] = "facility added successfully"
        conn.commit()
        cur.close()
        conn.close()
        return redirect('dashboard')
        #return render_template('dashboard.html', username=session['username'], error=good)
    return render_template('add_facility.html', error=error)

@app.route("/add_asset", methods=('GET', 'POST'))
def add_asset():
    error = None
    conn = psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
    cur = conn.cursor()
    cur.execute("select code from facilities;")
    facilities = cur.fetchall()
    if request.method=='GET':
        return render_template('add_asset.html', facilities=facilities)
    if request.method=='POST':
        tag = request.form['tag']
        description = request.form['description']
        facility_code = request.form['facility_code']
        conn =  psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
        cur = conn.cursor()
        cur.execute("select count(*) from assets where asset_tag=(%s);", (tag, ))
        count = cur.fetchone()[0]
        if count != 1:
            cur.execute("insert into assets (asset_tag, description) values (%s, %s);", (tag, description))
            cur.execute("insert into asset_at (asset_fk, facility_fk) select asset_pk, facility_pk from assets a, facilities f where a.asset_tag=%s and f.code=%s;", (tag, facility_code))
            session['error'] = "asset added successfully"
            conn.commit()
        else:
            session['error'] = "duplicate asset"
            return redirect('dashboard.html')
        cur.close()
        conn.close()
        return redirect('dashboard')
        # return render_template('add_asset.html', good=good, facilities=facilities)
    return render_template('add_asset.html', error=error)

@app.route("/dispose_asset", methods=('GET', 'POST'))
def dispose_asset():
    error = None
    conn =  psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
    cur = conn.cursor()
    cur.execute("select role_fk from users where user_pk=%s;", (session['username'], ))
    role_fk = cur.fetchone()[0]
    if role_fk != 1:
        error = "only Logistics Officers can approve transfers"
        return render_template('error.html', error=error)
    if request.method=='GET':
        cur.execute("select asset_tag from assets where disposed is NULL;")
        assets = cur.fetchall()
        return render_template('dispose_asset.html', assets=assets)
    if request.method=='POST':
        asset_tag = request.form['asset_tag']
        conn =  psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
        cur = conn.cursor()
        cur.execute("select asset_pk from assets where asset_tag=%s;", (asset_tag, ))
        asset_pk = cur.fetchone()[0]
        cur.execute("update asset_at set depart_dt=now() where asset_fk=%s;", (asset_pk, ))
        cur.execute("update assets set disposed=now() where asset_tag=%s;", (asset_tag, ))
        session['error'] = "asset disposed"
        conn.commit()
        cur.close()
        conn.close()
        return redirect('dashboard')
    return render_template('dispose_asset.html', error=error)

@app.route("/asset_report", methods=('GET', 'POST'))
def asset_report():
    return render_template('asset_report.html')

@app.route("/transfer_report", methods=('GET', 'POST'))
def transfer_report():
    return render_template('transfer_report.html')

@app.route("/transfer_req", methods=('GET', 'POST'))
def transfer_req():
    error = None
    conn =  psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
    cur = conn.cursor()
    cur.execute("select role_fk from users where user_pk=%s;", (session['username'], ))
    role_fk = cur.fetchone()[0]
    if role_fk != 1:
        error = "only Logistics Officers can request transfers"
        return render_template('error.html', error=error)
    if request.method=='GET':
        cur.execute("select asset_tag from assets where disposed is NULL;")
        session['assets'] = cur.fetchall()
        cur.execute("select code from facilities;")
        session['facilities'] = cur.fetchall()
        return render_template('transfer_req.html', assets=session['assets'], facilities=session['facilities'])
    if request.method=='POST':
        asset_tag = request.form['asset_tag']
        facility_code = request.form['destination_facility']
        requester = session['username']
        summary = request.form['summary']
        cur.execute("select asset_pk from assets where asset_tag=%s;", (asset_tag, ))
        asset_fk = cur.fetchone()[0]
        cur.execute("select facility_pk from facilities where code=%s;", (facility_code, ))
        destination_facility = cur.fetchone()[0]
        cur.execute("select count(*) from asset_at where asset_fk=%s and facility_fk=%s;", (asset_fk, destination_facility, ))
        count = cur.fetchone()[0]
        if count == 0:
            cur.execute("select facility_fk from asset_at where asset_fk=%s;", (asset_fk, ))
            source_facility = cur.fetchone()[0]
            cur.execute("insert into transit_request (requester, asset_fk, source_facility_fk, destination_facility_fk, summary) values (%s, %s, %s, %s, %s);", (requester, asset_fk, source_facility, destination_facility, summary, ))
            session['error'] = "transfer request created successfully"
            conn.commit()
            cur.close()
            conn.close()
            return redirect('dashboard')
            #return render_template('transfer_req.html', good=good, assets=session['assets'], facilities=session['facilities'])
        else:
            session['error'] = "that asset is already at that facility.  Try again."
            return redirect('dashboard')
    return render_template('transfer_req.html', error=error)

@app.route("/approve_req", methods=('GET', 'POST'))
def approve_req():
    error = None
    conn =  psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
    cur = conn.cursor()
    cur.execute("select role_fk from users where user_pk=%s;", (session['username'], ))
    role_fk = cur.fetchone()[0]
    if role_fk != 2:
        error = "only Facilities Officers can approve transfers"
        return render_template('error.html', error=error)
    if request.method=='GET':
        cur.execute("select request_pk, summary, requester from transit_request where approved_by is NULL;")
        info = cur.fetchall()
        cur.execute("select count(*) from transit_request where approved_by is NULL;")
        count = cur.fetchone()[0]
        if count == 1:
            return render_template('approve_req.html', info=info)
        return render_template('approve_req.html', info=info, count=count)
    if request.method=='POST':
        request_pk = request.form['transfer_request']
        if request.form['option'] == 'Reject':
            cur.execute("delete from transit_request where request_pk=%s;", (request_pk, ))
            conn.commit()
            session['error'] = "You rejected the request and it was deleted"
            return redirect('dashboard')
        if request.form['option'] == 'Approve':
            cur.execute("update transit_request set approved_by=%s, approved_dt=now() where request_pk=%s;", (session['username'], request_pk, ))
            session['error'] = "transfer request approved"
            conn.commit()
            cur.close()
            conn.close()
            return redirect('dashboard')
if __name__ == "__main__":
    app.run()
