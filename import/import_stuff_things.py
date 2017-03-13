from flask import Flask, flash, redirect, render_template, request, session, abort
import json
import os
import pathlib
import psycopg2
import sys
import csv

dbname = sys.argv[1]
import_path = sys.argv[2]

conn =  psycopg2.connect(dbname=dbname, host="/tmp", port=5432)
cur = conn.cursor()



def importUsers():
	fullname = os.path.join(import_path,"users.csv")
	with open(fullname) as csvfile:
	    reader = csv.DictReader(csvfile)
	    for row in reader:
	    	role = 0
	    	if row['role'] == 'Logistics Officer':
	    		role = 1
	    	else:
	    		role = 2
	    		cur.execute("insert into users values (%s, %s, %s, %s);", (row['username'], row['password'], role, row['active'], ))
	    	conn.commit()

def importFacilities():
	fullname = os.path.join(import_path,"facilities.csv")
	with open(fullname) as csvfile:
	    reader = csv.DictReader(csvfile)
	    for row in reader:
	    	cur.execute("insert into facilities (name, code) values (%s, %s);", (row['fcode'], row['common_name'], ))
	    	conn.commit()

def importAssets():
	fullname = os.path.join(import_path,"assets.csv")
	count = 1
	with open(fullname) as csvfile:
	    reader = csv.DictReader(csvfile)
	    for row in reader:
	    	cur.execute("select facility_pk from facilities where code=%s;", (row['facility'], ))
	    	facility_fk = cur.fetchone()[0]
	    	cur.execute("insert into assets (asset_tag, description, disposed) values (%s, %s, %s);", (row['asset_tag'], row['description'], row['disposed'], ))
	    	cur.execute("insert into asset_at (asset_fk, facility_fk, arrive_dt) values (%s, %s, %s);", (count, facility_fk, row['acquired'], ))
	    	count += 1
	    	conn.commit()

def importTransfers():
	fullname = os.path.join(import_path,"transfers.csv")
	with open(fullname) as csvfile:
	    reader = csv.DictReader(csvfile)
	    for row in reader:
	    	cur.execute("select asset_pk from assets where asset_tag=%s;", (row['asset_tag'], ))
	    	asset_fk = cur.fetchone()[0]
	    	cur.execute("select facility_pk from facilities where code=%s;", (row['source'], ))
	    	source_fk = cur.fetchone()[0]
	    	cur.execute("select facility_pk from facilities where code=%s;", (row['destination'], ))
	    	destination_fk = cur.fetchone()[0]
	    	cur.execute("insert into transit_request (requester, create_dt, asset_fk, source_facility_fk, destination_facility_fk, approved_by, approved_dt, load_time, unload_time) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (row['request_by'], row['request_dt'], asset_fk, source_fk, destination_fk, row['approve_by'], row['approve_dt'], row['load_dt'], row['unload_dt'], ))
	    	conn.commit()




def main():
    importUsers()
    importFacilities()
    importAssets()
    importTransfers()
if __name__=='__main__':
    main()
