from flask import Flask, flash, redirect, render_template, request, session, abort
app = Flask(__name__)
 
@app.route("/")
def index():
    return render_template('login.html')
 
@app.route("/report_filter")
def hello():
    return render_template('reportQuery.html')
 
@app.route("/facility_inventory_report")
def getInventoryReports():
    return render_template('facilityInventory.html')
 
@app.route("/in_transit_report")
def getInTransitReports():				#can put variables in these functions 
    return render_template('inTransit.html')

@app.route("/logout")
def logout():
    return render_template('logout.html')
 
if __name__ == "__main__":
    app.run()