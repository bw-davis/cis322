from flask import Flask, flash, redirect, render_template, request, session, abort
import json
import os
import pathlib
import psycopg2
import sys
import csv

dbname = sys.argv[1]
export_path = sys.argv[2]

conn =  psycopg2.connect(dbname=dbname, host="/tmp", port=5432)
cur = conn.cursor()

def exportUsers():
	fullname = os.path.join(export_path,"users.csv")
	cur.execute("select * from users;")
	row = cur.fetchall()
	with open(fullname, 'w') as csvfile:
	    fieldnames = ['username', 'password', 'role', 'active']
	    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

	    writer.writeheader()
	    role = ''
	    for r in row:
	    	if r[2] == 1:
	    		role = 'Logistics Officer'
	    	else:
	    		role = 'Facilities Officer'
	    	writer.writerow({'username': r[0], 'password': r[1], 'role': role, 'active': 'TRUE'})

def exportFacilities():
	fullname = os.path.join(export_path,"facilities.csv")
	cur.execute("select * from facilities;")
	row = cur.fetchall()
	with open(fullname, 'w') as csvfile:
	    fieldnames = ['fcode', 'common_name']
	    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

	    writer.writeheader()
	    for r in row:
	    	writer.writerow({'fcode': r[1], 'common_name': r[2]})

def exportAssets():
	fullname = os.path.join(export_path,"assets.csv")
	cur.execute("select * from assets;")
	row = cur.fetchall()

	with open(fullname, 'w') as csvfile:
	    fieldnames = ['asset_tag', 'description', 'facility', 'acquired', 'disposed']
	    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

	    writer.writeheader()
	    disposed = ''
	    asset_at = []
	    for r in row:
	    	if r[3] == 'TRUE':
	    		cur.execute("select arrive_dt, depart_dt, facility_fk from asset_at where asset_fk=%s;", (r[0]))
	    		asset_at = cur.fetchall()
	    		disposed = asset_at[3]
	    	else:
	    		cur.execute("select arrive_dt, facility_fk from asset_at where asset_fk=%s;", (r[0], ))
	    		asset_at = cur.fetchall()
	    		disposed = 'NULL'
	    	cur.execute("select name from facilities where facility_pk=%s;", (asset_at[0][1], ))
	    	facility = cur.fetchone()[0]
	    	writer.writerow({'asset_tag': r[1], 'description': r[2], 'facility': facility, 'acquired': asset_at[0][0], 'disposed': disposed})

def main():
    exportUsers()
    exportFacilities()
    exportAssets()
    # with open('inv_load.sql','w') as f:
    #     process_inventory(f,sys.argv[1])

if __name__=='__main__':
    main()
