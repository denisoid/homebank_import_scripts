#!/usr/bin/python
# -*- coding: utf8 -*-

import sys, sqlite3, time, os.path


if len(sys.argv) != 2:
	print 'Need one argument -- path to data.db'
	exit()

#get filename
filename = sys.argv[1]

#connect to database
conn = sqlite3.connect(filename)

#query to get all expenses and categories names
query="""select * from expenses
left join categories on (expenses.category_id = categories.id)
where expenses.deleted = 0; """




#make cursor and load data to it
conn.row_factory=sqlite3.Row
cur=conn.cursor()
cur.execute(query)

#expenses divide to several dicts
accounts={}

#enumaration expenses
for row in cur:
	out=[]
	

	#print date
	timestamp=row['date']
	out.append(time.strftime('%d-%m-%y',time.localtime(timestamp)) )
	
	#print mode
	out.append('0')
	
	#print info
	out.append(row['note'])
	
	#print payee name
	out.append('')
	
	#print description
	out.append(row["title"])
	
	#print amount
	out.append(str(row["amount"]))

	#print category name
	out.append(row["name"])


	
	#glue list and print it
	line=u";".join(out)
	
	account_id=row["account_id"];
	
	if not account_id in accounts:
		accounts[account_id]=[]
	
	
	accounts[account_id].append(line.encode('utf-8'))
	#print line.encode('utf-8')
	
	
#saving to csv

basename=os.path.splitext(filename)[0];

	
for account_id in accounts:
	account_filename=basename + "_" + `account_id` + ".csv";
	filedata="\n".join(accounts[account_id]);
	

	
	
	fileObj = open(account_filename,"w")
	fileObj.write(filedata);
	fileObj.close()
	
	print account_id
#print accounts;
