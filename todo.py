#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# 2016-12-03 First complete version 1.1
# 2017-01-23 Minor syntax fix at help()


import sqlite3
import datetime
import sys
import datetime

DB = sqlite3.connect('./database/todo.db')
DB.row_factory = sqlite3.Row

### INFO ------------------------------------------------------------



### Extra functions -------------------------------------------------
def xxx_todo():
	html=""
	tasks=[
	["DB schema","Add support for ON DELETE and ON UPDATE","Waiting"],
	["Source code","Add support for translations","Waiting"],
	["/location/modify/TestLocation1","Result message of location modify is ugly","Waiting"],
	["/location/add","Result message of location add is too simple","Waiting"],
	["/box/show/","Add link to location information","Waiting"],
	["/box/add","Result message of box add is too simple","Waiting"],
	["Source code","When using status, variable name should be status_id","Waiting"],
	["/box/modify/","Validate occypancy as number 0..100","Waiting"],
	["/box/modify/","Resule message of box modify is too simple","Waiting"],
	["/location/modify","Validate all input fields","Waiting"],
	["/box/modify","Validate all input fields","Waiting"],
	["/item/modify","Validate all input fields","Waiting"],
	["/location/add","Validate all input fields","Waiting"],
	["/box/add","Validate all input fields","Waiting"],
	["/item/add","Validate all input fields","Waiting"],
	["Source code","Create simple TODO functionality","Done"],
	["/item/add","Implement functionality","Done"],
	["/item/modify","Implement functionality","WIP"]
	]
	
	for t in tasks:
		arg=["a","a"]
		arg.append(t[0])
		arg.append(t[1])
		arg.append("")
		print(arg)
		add(arg)
		
### Database functions ..---------------------------------------------
def db_execute(mode,sql,sql_parameters):
	"""Run SQL commands"""
	
	#print(mode,sql,sql_parameters.encode('utf8'))	
	
	c = DB.cursor()
	c_status = c.execute(sql,sql_parameters)
	if mode == "readall":
		result = c.fetchall()
	elif mode == "readone":
		result = c.fetchone() 
	elif mode == "write":
		result = c_status
		DB.commit()
	else:
		raise ValueError("Unknown mode")	
	c.close()  
	return(result)

### -----------------------------------------------------------------
def initialize_database():
	sql=[	'DROP TABLE IF EXISTS todo',
			'--',
			'CREATE TABLE todo (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, target TEXT NOT NULL, name TEXT NOT NULL, description TEXT , status INTEGER NOT NULL DEFAULT 0, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL)',
			'--INSERT INTO todo (target, name, description) VALUES ("Test","Test1","No location selected")',
			'--INSERT INTO todo (target, name, description) VALUES ("Test2","Test2","Location selected")',
			'--'
		]
	# Unicode values
	# ä = \u00E4
	# ö = \u00F6
	
	print ("Alustetaan tietokanta")
	try:
		for s in sql:
			print(s)
			c=db_execute("write",s,"")
	except sqlite3.OperationalError as e:
		print ("FAIL : "+ str(e))
	except sqlite3.IntegrityError as e:
		print ("FOREING KEY FAIL : "+ str(e))
	
### -----------------------------------------------------------------	
def get_tasks(id):

	if id==0:
		sql="SELECT id,target,name,description,status FROM todo ORDER BY status"
		return(db_execute("readall",sql,""))
	elif id.isdigit():
		sql="SELECT id,target,name,description,status FROM todo WHERE id=? ORDER BY status,id"
		return(db_execute("readall",sql,id))
	elif id.lower() in ("new","n","wip","w","done","d","cancelled","c","hold","h"):
		status=-1
		if id.lower()[:1]=="n":
			status="0"
		elif id.lower()[:1]=="w":
			status="1"
		elif id.lower()[:1]=="d":
			status="2"
		elif id.lower()[:1]=="c":
			status="3"
		elif id.lower()[:1]=="h":
			status="4"	

		sql="SELECT id,target,name,description,status FROM todo WHERE status=? ORDER BY id"
		return(db_execute("readall",sql,status))
		
### -----------------------------------------------------------------
def get_status_text(status):
	"""
	Task state 		Possible new states
	0 - New			1,3,4
	1 - WIP			2,3,4
	2 - Done		
	3 - Cancelled	0,1
	4 - Hold	 	1
	"""
	if status==0:
		return("New")
	elif status==1:
		return("WIP")
	elif status==2:
		return("Done")
	elif status==3:
		return("Cancelled")
	elif status==4:
		return("Hold")

### -----------------------------------------------------------------
def help():
	help=[	"How to use SimpleTODO:",
			"Commands:",
			"   Add new task......... add <target> <name> <description>",
			"                         a <target> <name> <description>",
			"   Show all tasks....... show",
			"                         s",
			"   Show task by id...... show <task id>",
			"                         s <task id>",
			"   Show task by status.. show <new|wip|done|cancelled|hold>",
			"                         s <n|w|d|c|h>",
			"   Modify task.......... modify target <task id> <new target>",
			"                         m t <task id> <new target>",
			"                         modify name <task id> <new name>",
			"                         m n <task id> <new target>",
			"                         modify description <new description> ",
			"                         m d <task id> <new description>",
			"                         modify state <task id> <new status>",
			"                         m s <task id> <new status>",
			"   Initialize database.. initialize <current hours> <current minutes>"]
	
	for l in help:
		print(l)
		
	exit(1)

### -----------------------------------------------------------------
def main():
	if len(sys.argv)<=1 or len(sys.argv)>=6:
		help()
	else:
		select_command(sys.argv[1],sys.argv)		
	
#### ----------------------------------------------------------------
def select_command(cmd,arg):
	cmd_functions={ "add": add,
					"a": add,
					"show": show,
					"s": show,
					"modify": modify,
					"m": modify,
					"initialize": initialize,
					"i": initialize }

	cmd=cmd.lower()

	try:
		cmd_functions[cmd](arg)
		exit(0)
	except Exception:
		help()
		
### -----------------------------------------------------------------
def add(arg):
	print("Add")
	if len(arg)==5:
		print("New task")
		task_target=arg[2]
		task_name=arg[3]
		task_description=arg[4]
		print("Target.......",task_target)
		print("Name.........",task_name)
		print("Description..",task_description)
		
		# Check for duplicate task
		sql ="SELECT id FROM todo WHERE target=? AND name=? AND description=?"
		c=db_execute("readall",sql,[task_target, task_name, task_description])
		if len(c)!=0:
			print("ERROR: Can't add duplicate task")
			exit(1)
		
		sql="INSERT INTO todo (target, name, description) VALUES (?,?,?)"
		c=db_execute("write",sql,[task_target, task_name, task_description])
		
		sql="SELECT last_insert_rowid() as last_id FROM todo"
		last=db_execute("readone",sql,"")
		
		print("Task id......",last["last_id"])
		
	else:
		help()
	
	
### -----------------------------------------------------------------
def show(arg):
	print("Show")
	if len(arg)==2: # show all
		sql="SELECT MAX(LENGTH(id)) AS id, MAX(LENGTH(target)) AS target, MAX(LENGTH(name)) AS name, MAX(LENGTH(description)) AS description FROM todo"
		col_lens=db_execute("readone",sql,"")
		show_print("All tasks",col_lens,get_tasks(0))
		
	elif len(arg)==3 and not arg[2].isdigit(): # show <task status>
		status = arg[2].lower()
		num_status=-1
		if status in ("0","new","n"):
			num_status=0
			status="New"
		elif status in ("1","wip","w"):
			num_status=1
			status="WIP"
		elif status in ("2","done","d"):
			num_status=2
			status="Done"
		elif status in ("3","cancelled","c"):
			num_status=3
			status="Cancelled"
		elif status in ("4","hold","h"):
			num_status=4
			status="Hold"
		else:
			help()
	
		sql="SELECT MAX(LENGTH(id)) AS id, MAX(LENGTH(target)) AS target, MAX(LENGTH(name)) AS name, MAX(LENGTH(description)) AS description FROM todo"
		col_lens=db_execute("readone",sql,"")
		show_print("Tasks with status:"+status,col_lens,get_tasks(status))
		
	elif len(arg)==3 and arg[2].isdigit(): # show <task id>
		sql="SELECT MAX(LENGTH(id)) AS id, MAX(LENGTH(target)) AS target, MAX(LENGTH(name)) AS name, MAX(LENGTH(description)) AS description FROM todo"
		col_lens=db_execute("readone",sql,"")
		show_print("Task:"+arg[2],col_lens,get_tasks(arg[2]))
	else:
		help()
		
### -----------------------------------------------------------------
def show_print(title,col_lens,tasks):
	print(title)
	print (		('{:%s}'%(10)).format("STATUS"),
				('{:%s}'%(col_lens["id"])).format("ID"),
				('{:%s}'%(col_lens["target"]+1)).format("TARGET"),
				('{:%s}'%(col_lens["name"]+1)).format("NAME"),
				('{:%s}'%(col_lens["description"]+1)).format("DESCRIPTION"),
				)

	for t in tasks:
		print (		('{:10}'.format(get_status_text(t["status"]))),	
					('{:%s}'%(col_lens["id"])).format(t["id"]),
					('{:%s}'%(col_lens["target"]+1)).format(t["target"]),
					('{:%s}'%(col_lens["name"]+1)).format(t["name"]),
					('{:%s}'%(col_lens["description"]+1)).format(t["description"])
					)
			
			
### -----------------------------------------------------------------
def modify(arg):
	print("Modify")
	if len(arg)!=5:
		help()
		exit(1)
		
	if arg[2]=="target" or arg[2]=="t":
		print("Target")
		task_id = arg[3]
		new_target = arg[4]
		print ("Task id.....", task_id)
		print ("New target..", new_target)
		sql="UPDATE todo SET target=? WHERE id=?"
		last=db_execute("write",sql,[new_target, task_id])
	elif arg[2]=="name" or arg[2]=="n":
		print("Name")
		task_id = arg[3]
		new_name = arg[4]
		print ("Task id.....", task_id)
		print ("New name...", new_name)
		sql="UPDATE todo SET name=? WHERE id=?"
		last=db_execute("write",sql,[new_name, task_id])	
	elif arg[2]=="description" or arg[2]=="d":
		print("Description")
		task_id = arg[3]
		new_desc = arg[4]
		print ("Task id..........", task_id)
		print ("New description..", new_desc)
		sql="UPDATE todo SET description=? WHERE id=?"
		last=db_execute("write",sql,[new_desc, task_id])
	elif arg[2]=="state" or arg[2]=="s":
		print("Status")
		task_id = arg[3]
		new_status = arg[4].lower()
		num_status=-1
		
		if new_status in ("0","new","n"):
			num_status=0
			new_status="New"
		elif new_status in ("1","WIP","w"):
			num_status=1
			new_status="WIP"
		elif new_status in ("2","done","d"):
			num_status=2
			new_status="Done"
		elif new_status in ("3","cancelled","c"):
			num_status=3
			new_status="Cancelled"
		elif new_status in ("4","hold","h"):
			num_status=4
			new_status="Hold"
		else:
			help()
			
		print ("Task id.....", task_id)
		print ("New status..", new_status)
		
		sql="UPDATE todo SET status=? WHERE id=?"
		last=db_execute("write",sql,[num_status, task_id])	

### -----------------------------------------------------------------
def initialize(arg):
	print("Initialize")
	now = datetime.datetime.now()
	print ("Current hour:",now.hour)
	print ("Current minute:",now.minute)
	try:
		print ("Your hour:", arg[2])
		print ("Your minute:", arg[3])
	except Exception:
		pass
	
	if len(arg)==4 and arg[2]==str(now.hour) and arg[3]==str(now.minute):
		initialize_database()
	else:
		print("ERROR: Can't initilaize database")	
	
#### ----------------------------------------------------------------
if __name__=='__main__':
	main()
	#xxx_todo()