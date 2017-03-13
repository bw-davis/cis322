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
	#with open(fullname, 'w') as csvfile:
	with open(fullname) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print(row['username'], row['password'], row['role'], row['active'])
def importFacilities():
	fullname = os.path.join(import_path,"facilities.csv")
	#with open(fullname, 'w') as csvfile:
	with open(fullname) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print(row['fcode'], row['common_name'])
def importAssets():
	fullname = os.path.join(import_path,"assets.csv")
	#with open(fullname, 'w') as csvfile:
	with open(fullname) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print(row['asset_tag'], row['description'], row['facility'], row['aquired'], row['disposed'])
def importTransfers():
	fullname = os.path.join(import_path,"transfers.csv")
	#with open(fullname, 'w') as csvfile:
	with open(fullname) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print(row['asset_tag'], row['request_by'], row['request_dt'], row['approve_by'], row['approve_dt'], row['source'], row['destination'], row['load_dt'], row['unload_dt'])




def main():
    importUsers()
    importFacilities()
    importAssets()
    importTransfers()
if __name__=='__main__':
    main()