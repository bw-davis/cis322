import sys
import csv

first_arg = sys.argv[1]

f1 = open(first_arg)  #the code for DC_inventory.csv
csv_f = csv.reader(f1)
col_1 = list(zip(*csv_f))
# print(col_1)
dcInventoryList = []
for row in col_1:
	dcInventoryList.append(row)

asset_pk = []
skip_name = True
for word in dcInventoryList[0]:
	if not skip_name:
		asset_pk.append(word)
	else :
		skip_name = False

compartment_pk = []
skip_name = True
for word in dcInventoryList[3]:
	if not skip_name:
		compartment_pk.append(word)
	else :
		skip_name = False

print(asset_pk)
print(compartment_pk)

