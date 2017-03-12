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
	target_dir = export_path
	fullname = os.path.join(target_dir,"users.csv")
	cur.execute("select * from users;")
	row = cur.fetchall()
	with open(fullname, 'w') as csvfile:
	    fieldnames = ['username', 'password', 'role', 'active']
	    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

	    writer.writeheader()
	    for r in row:
	    	writer.writerow({'username': r[0], 'password': r[1], 'role': r[2], 'active': 'True'})
	    	
def main():
    exportUsers()
    # with open('inv_load.sql','w') as f:
    #     process_inventory(f,sys.argv[1])

if __name__=='__main__':
    main()