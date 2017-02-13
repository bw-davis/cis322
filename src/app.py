from flask import Flask, flash, redirect, render_template, request, session, abort
import json
app = Flask(__name__)
 
@app.route("/")
def index():
    return render_template('login.html')
 
@app.route("/report_filter")
def hello():
    return render_template('reportQuery.html')

@app.route("/rest")
def rest():
	return render_template('rest.html')

@app.route("/rest/lost_key", methods=('POST',))
def rest_key():
    if request.method=='POST' and 'arguments' in request.form:
        data=request.form['arguments']
    return returnJson(theRequest)

@app.route("/rest/activate_user", methods=('POST',))
def activate_user():
    if request.method=='POST' and 'arguments' in request.form:
        data=request.form['arguments']
    return returnJson(theRequest)

@app.route('/rest/suspend_user', methods=('POST',))
def suspend_user():
    if request.method=='POST' and 'arguments' in request.form:
        theRequest=json.loads(request.form['arguments'])
    return returnJson(theRequest)

@app.route("/rest/list_products", methods=('POST',))
def list_products():
    if request.method=='POST' and 'arguments' in request.form:
        data=request.form['arguments']
    return returnJson(theRequest)

@app.route("/rest/add_products", methods=('POST',))
def add_products():
    if request.method=='POST' and 'arguments' in request.form:
        data=request.form['arguments']
    return returnJson(theRequest)

@app.route("/rest/add_asset", methods=('POST',))
def add_asset():
    if request.method=='POST' and 'arguments' in request.form:
        data=request.form['arguments']
    return returnJson(theRequest)

@app.route("/facility_inventory_report")
def getInventoryReports():
    return render_template('facilityInventory.html')
 
@app.route("/in_transit_report")
def getInTransitReports():				#can put variables in these functions 
    return render_template('inTransit.html')

@app.route("/logout")
def logout():
    return render_template('logout.html')

def returnJson(req):
    theData = dict()
    theData['timestamp'] = req['timestamp']
    theData['result'] = 'OK'
    returnJson = json.dumps(theData)
    return theData
 
if __name__ == "__main__":
    app.run()