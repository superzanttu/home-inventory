#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import bottle
import sqlite3
import datetime
import os
import csv
import codecs
import urllib.parse

# My own modules
import checksum
import todo

app = bottle.app()
#bottle.install(SQLitePlugin(dbfile='./hiapp.db'))

DB = sqlite3.connect('./database/hiapp.db')
DB.row_factory = sqlite3.Row

### HTML functions --------------------------------------------------
@app.error(403)
def mistake403(code):
	return 'Incorrect parameter format!'

@app.error(404)
def mistake404(code):
	#app.redirect("/")
	return ("Can't find page")

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

### Helpper functions -----------------------------------------------
def get_all_items(cid):
	"""Return recursively all items of starting from selected container"""
	sql="WITH RECURSIVE list (lid) AS ( \
		SELECT id FROM containers WHERE id='%s' \
		UNION \
		SELECT id FROM containers, list \
		WHERE containers.container_id = list.lid ) \
		SELECT * FROM items WHERE container_id IN list and status=1" % (cid)
	return(db_execute("readall",sql,""))

def get_page_start():
	"""Generate header for HTML-page"""
	html="<!DOCTYPE html><html><head>"
	html+="<title>Home inventory</title>"
	html+="</head>"
	html+="<body>"
	html+='<font face="arial, verdana, sans-serif">'
	html+=get_simple_menu()

	tasks=todo.get_tasks("wip")
	if tasks and False:
		html+="<br>"
		html+="<table><tr><th>ID</th><th>TARGET</th><th>NAME</th><th>DESCRIPTION</th></tr>"
		for t in tasks:
			html+="<tr><th>"+str(t["id"])+"</th><th>"+t["target"]+"</th><th>"+t["name"]+"</th><th>"+t["description"]+"</th></tr>"
		html+="</table>"
		html+="<br>"

	bottle.content_type="text/html; charset=utf-8"
	return(html)

### -----------------------------------------------------------------
def get_page_end():
	"""Generate footer for HTML-page"""
	html="</font></body></html>"
	return(html)

### -----------------------------------------------------------------
def get_simple_menu():
	"""Generate simple command menu"""
	admin_menu=["Admin",[["",""]]]
	start_menu=["Start",[["World","/world/"]]]
	add_menu=["Add",[["Building","/add/building/"],["Room","/add/room/"],["Shelves","/add/shelves/"],["Shelf","/add/shelf/"],["Box","/add/box/"],["Item","/add/item/"]]]
	delete_menu=["Delete",[["Container","/delete/container/"],["Item","/delete/item/"]]]
	modify_menu=["Modify",[["",""]]]
	management_menu=["Management",[["Import CSV","/import/"],["Export CSV","/export"]]]
	user_menu=["User",[["Logout","/logout"]]]
	annotations_menu=["Annotations",[["Annotations","/annotations/list/"],["Annotation lists","/annotation_lists/list/"]]]

	menu_order = [admin_menu, start_menu, add_menu, annotations_menu, delete_menu, modify_menu, management_menu, user_menu]

	# Show simple menu
	html="<table>"
	html+='<tr><th align="left"><a href="/">Home</a></th></tr>'
	for m in menu_order:
		html+='<tr><th align="left">'+m[0]+'</th>'
		for n in m[1]:
			html+='<th align="left"><a href="'+n[1]+'">'+n[0]+'</a></th>'
		html+="</tr>"
	html+="</table>"
	return(html)


### PAGE FUNCTIONS --------------------------------------------------
### Home page -------------------------------------------------------
@app.route('/')
def home():
	html=get_page_start()
	if bottle.request.get_cookie("logged"):
		html+="<p>Logged in?</p>"
	else:
		bottle.redirect("/login")

	html+=get_page_end()
	return (html)


### Login & logout --------------------------------------------------
@app.get('/login') # or @route('/login')
def login_form():
	"""Ask for username and password"""
	html=get_page_start()
	html+=('''
<form action="/login" method="post">
	Käyttäjä: <input name="username" type="text" />
	Salasana: <input name="password" type="password" />
	<input value="Kirjaudu" type="submit" />
</form>
	''')
	html+=get_page_end()
	return(html)

@app.post('/login') # or @route('/login', method='POST')
def login_form_check():
	"""Check username and password from login form"""
	username = bottle.request.forms.get('username')
	password = bottle.request.forms.get('password')
	if username=='guru' and password=='guru':
		bottle.response.set_cookie("logged", "yes")
		bottle.redirect("/")
		#return ("<p>Your login information was correct.</p>")
	else:
		return ("<p>Tunnus tai salasana ei kelpaa.</p>")

@app.route('/logout')
def do_logout():
	"""Log user out"""
	bottle.response.delete_cookie("logged")
	bottle.redirect('/')
	#return("Logout")


##########################################################################################
# FIXME
@app.post('/item/upload_picture/<id:re:\w+>')
def upload_item_picture(id):
	upload	   = bottle.request.files.get('item_picture')
	name, ext = os.path.splitext(upload.filename)
	if ext not in ('.png','.jpg','.jpeg'):
		return ('File extension %s not allowed.' % (ext))

	save_path = "/hiapp/pictures/%s_%s" % (id,upload.filename)
	upload.save(save_path) # appends upload.filename automatically
	return ('<html><img src="%s"></html>' % (save_path + upload.filename))


##########################################################################################
"""Import CSV files into database"""
@app.route('/import/')
@app.post('/import/')
def import_csv():
	html=get_page_start()
	if bottle.request.POST.importcsv:
		csv_file1 = bottle.request.files.get('csvfile')
		name, ext = os.path.splitext(csv_file1.filename)
		targettable = bottle.request.forms.get('targettable').strip()
		html+="<p>CSV file name: %s%s</p>" % (name, ext)
		html+="<p>Target table: %s</p>" % (targettable)

		csv_file2 = bottle.request.files.csvfile.file
		csv_reader= csv.reader(codecs.iterdecode(csv_file2, 'utf-8'), delimiter=',')

		# Check header format
		firstrow=next(csv_reader)
		fileFormatOk=False
		if ext not in ('.csv','.CSV'):
				html+='<p>ERROR: File extension %s not allowed.</p>' % (ext)
		elif targettable == "containers": # Containers
			if firstrow[0]!="CONTAINER_ID" or firstrow[1]!="CONTAINER_TYPE" or firstrow[2]!='LOCATION_ID' or firstrow[3]!='CONTAINER_NAME' or firstrow[4]!='CONTAINER_STATUS':
				html+="<p>ERROR: CSV file header incorrect</p>"
				html+="<p>Correct header is 'CONTAINER_ID,CONTAINER_TYPE,LOCATION_ID,CONTAINER_NAME,CONTAINER_STATUS'</p>"
				html+="<p>%s</p>" % firstrow[1]
			else:
				fileFormatOk=True
				html+="<p>%s</p>" % firstrow
				html+="<p>CSV file header OK</p>"
		elif targettable == "items": # items
			if firstrow[0]!="ITEM_ID" or firstrow[1]!='LOCATION_ID' or firstrow[2]!='ITEM_NAME' or firstrow[3]!='ITEM_STATUS':
				html+="<p>ERROR: CSV file header incorrect</p>"
				html+="<p>Correct header is 'ITEM_ID,LOCATION_ID,ITEM_NAME,ITEM_STATUS'</p>"
				html+="<p>%s</p>" % firstrow[1]
			else:
				fileFormatOk=True
				html+="<p>%s</p>" % firstrow
				html+="<p>CSV file header OK</p>"
		elif targettable == "shelfs": # items
			if firstrow[0]!="SHELF_ID" or firstrow[1]!='SHELF_COLUMN' or firstrow[2]!='SHELF_ROW' or firstrow[3]!='SHELF_TYPE':
				html+="<p>ERROR: CSV file header incorrect</p>"
				html+="<p>Correct header is 'SHELF_ID,SHELF_COLUMN,SHELF_ROW,SHELF_TYPE'</p>"
				html+="<p>%s</p>" % firstrow[1]
			else:
				fileFormatOk=True
				html+="<p>%s</p>" % firstrow
				html+="<p>CSV file header OK</p>"
		elif targettable == "annotations": # annotations
			if firstrow[0]!="ANNOTATION_ID" or firstrow[1]!='ANNOTATION_TYPE' or firstrow[2]!='ANNOTATION_LIST_ID' or firstrow[3]!='ANNOTATION_TEXT' or firstrow[4]!='ANNOTATION_STATUS':
				html+="<p>ERROR: CSV file header incorrect</p>"
				html+="<p>Correct header is 'ANNOTATION_ID,ANNOTATION_TYPE,ANNOTATION_LIST_ID,ANNOTATION_TEXT,ANNOTATION_STATUS'</p>"
				html+="<p>%s</p>" % firstrow[1]
			else:
				fileFormatOk=True
				html+="<p>%s</p>" % firstrow
				html+="<p>CSV file header OK</p>"
		elif targettable == "annotation_lists": # annotation_lists
			if firstrow[0]!="ANNOTATION_LIST_ID" or firstrow[1]!='LIST_ITEM':
				html+="<p>ERROR: CSV file header incorrect</p>"
				html+="<p>Correct header is 'ANNOTATION_LIST_ID,LIST_ITEM'</p>"
				html+="<p>%s</p>" % firstrow[1]
			else:
				fileFormatOk=True
				html+="<p>%s</p>" % firstrow
				html+="<p>CSV file header OK</p>"
		elif targettable == "item_annotations": # annotations
			if firstrow[0]!="ITEM_ID" or firstrow[1]!='ANNOTATION_ID' or firstrow[2]!='ANNOTATION_VALUE':
				html+="<p>ERROR: CSV file header incorrect</p>"
				html+="<p>Correct header is 'ITEM_ID,ANNOTATION_ID,ANNOTATION_VALUE'</p>"
				html+="<p>%s</p>" % firstrow[1]
			else:
				fileFormatOk=True
				html+="<p>%s</p>" % firstrow
				html+="<p>CSV file header OK</p>"
		else:
			html+="ERROR: Unknown target table (%s) - Not implemented?" % targettable

		if fileFormatOk == True:
			# Import data
			if targettable == "containers": # Containers
				try:
					# DROP OLD TABLE
					c=db_execute("write","DROP TABLE IF EXISTS containers","")
					# CREATE NEW TABLE
					c=db_execute("write","CREATE TABLE containers ( id TEXT PRIMARY KEY NOT NULL, \
												type TEXT NOT NULL, \
												container_id TEXT NOT NULL, \
												name TEXT NOT NULL, \
												status INTEGER NOT NULL DEFAULT 1, \
												timestamp DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL)","")
					for r in csv_reader:
						if r[0]!="":
							sql="INSERT INTO containers (id, type, container_id, name, status) VALUES (?,?,?,?,?)"
							sql_p =[r[0],r[1],r[2],r[3],r[4]]
							html+="%s <br>" % (r)
							c=db_execute("write",sql,sql_p)
					html+="<p>Containers CSV imported</p>"
				except:
					html+="<p>ERROR: Containers CSV import error</p>"

			elif targettable == "items": # Items
				try:
					# DROP OLD TABLE
					c=db_execute("write","DROP TABLE IF EXISTS items","")
					# CREATE NEW TABLE
					c=db_execute("write","CREATE TABLE items (	id TEXT PRIMARY KEY NOT NULL, \
												container_id TEXT NOT NULL, \
												name TEXT NOT NULL, \
												status INTEGER NOT NULL DEFAULT 1, \
												timestamp DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL)","")
					for r in csv_reader:
						if r[0]!="":
							sql="INSERT INTO items (id, container_id, name, status) VALUES (?,?,?,?)"
							sql_p =[r[0],r[1],r[2],r[3]]
							html+="%s <br>" % (r)
							c=db_execute("write",sql,sql_p)
					html+="<p>Items CSV imported</p>"
				except:
					html+="<p>ERROR: Items CSV import error</p>"

			elif targettable == "shelfs": # Shelfs
					try:
						# DROP OLD TABLE
						c=db_execute("write","DROP TABLE IF EXISTS shelfs","")
						# CREATE NEW TABLE
						c=db_execute("write","CREATE TABLE shelfs ( id TEXT PRIMARY KEY NOT NULL, \
												column TEXT NOT NULL, \
												row TEXT NOT NULL, \
												type TEXT NOT NULL, \
												timestamp DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL)","")
						for r in csv_reader:
							if r[0]!="":
								sql="INSERT INTO shelfs (id, column, row, type) VALUES (?,?,?,?)"
								sql_p =[r[0],r[1],r[2],r[3]]
								html+="%s <br>" % (r)
								c=db_execute("write",sql,sql_p)
						html+="<p>Shelfs CSV imported</p>"
					except:
						html+="<p>ERROR: Shelfs CSV import error</p>"

			elif targettable == "annotations": # annotations
					try:
						# DROP OLD TABLE
						c=db_execute("write","DROP TABLE IF EXISTS annotations","")
						# CREATE NEW TABLE
						c=db_execute("write","CREATE TABLE annotations ( id TEXT PRIMARY KEY NOT NULL, \
												type TEXT NOT NULL, \
												list_id TEXT NOT NULL, \
												text TEXT NOT NULL, \
												status TEXT NOT NULL, \
												timestamp DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL)","")
						for r in csv_reader:
							if r[0]!="":
								sql="INSERT INTO annotations (id, type, list_id, text, status) VALUES (?,?,?,?,?)"
								sql_p =[r[0],r[1],r[2],r[3],r[4]]
								html+="%s <br>" % (r)
								c=db_execute("write",sql,sql_p)
						html+="<p>Annotations CSV imported</p>"
					except:
						html+="<p>ERROR: Annotations CSV mport error</p>"

			elif targettable == "annotation_lists": # annotation_lists
					try:
						# DROP OLD TABLE
						c=db_execute("write","DROP TABLE IF EXISTS annotation_lists","")
						# CREATE NEW TABLE
						c=db_execute("write","CREATE TABLE annotation_lists ( id TEXT NOT NULL, \
													item TEXT NOT NULL, \
													timestamp DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL)","")
						for r in csv_reader:
							if r[0]!="":
								sql="INSERT INTO annotation_lists (id, item) VALUES (?,?)"
								sql_p =[r[0],r[1]]
								html+="%s <br>" % (r)
								c=db_execute("write",sql,sql_p)
						html+="<p>Annotation lists CSV imported</p>"
					except:
						html+="<p>ERROR: Annotations lists CSV import error</p>"

			elif targettable == "item_annotations": # item_annotations
					try:
						# DROP OLD TABLE
						c=db_execute("write","DROP TABLE IF EXISTS item_annotations","")
						# CREATE NEW TABLE
						c=db_execute("write","CREATE TABLE item_annotations ( item_id TEXT NOT NULL, \
													annotation_id TEXT NOT NULL, \
													value TEXT NOT NULL, \
													timestamp DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL, \
													UNIQUE(item_id, annotation_id))","")
						for r in csv_reader:
							if r[0]!="":
								sql="INSERT INTO item_annotations (item_id, annotation_id, value) VALUES (?,?,?)"
								sql_p =[r[0],r[1],r[2]]
								html+="%s <br>" % (r)
								c=db_execute("write",sql,sql_p)
						html+="<p>Item annotations CSV imported</p>"
					except:
						html+="<p>ERROR: Item annotations CSV import error</p>"

	else:
		html+=bottle.template('templates/import_csv.tpl')

	html+=get_page_end()
	return(html)
	
	
##########################################################################################
@app.route('/add/building/')
@app.post('/add/building/')
def add_building():

	html=get_page_start()
	if bottle.request.POST.button_add_building:
		# Building Name and ID must be unique
		new_building_name = bottle.request.forms.get('new_building_name').strip()
		new_building_id = bottle.request.forms.get('new_building_id').strip()

		sql="SELECT * FROM containers WHERE type='BUILDING' AND (id=? OR name=?)"
		sql_p=[new_building_id,new_building_name]

		b = db_execute("readone",sql,sql_p)
		if b:
			html+="<p>ERROR: building name and id must be unique</p>"
		else:
			html+="<p>OK: building name and id are unique</p>"
			sql="INSERT INTO containers (id, type, container_id, name, status) VALUES (?,?,?,?,?)"
			sql_p=[new_building_id,"BUILDING","WORLD",new_building_name,1]
			c=db_execute("write",sql,sql_p)
			html+="<p>OK: new building added</p>"
	else:
		html+=bottle.template('templates/add_building.tpl')

	html+=get_page_end()
	return(html)


##########################################################################################
@app.route('/add/room/')
@app.post('/add/room/')
def add_room():

	html=get_page_start()
	if bottle.request.POST.button_add_room:
		# Building Name and ID must be unique
		new_room_name = bottle.request.forms.get('new_room_name').strip()
		new_room_id = bottle.request.forms.get('new_room_id').strip()
		selected_building_id = bottle.request.forms.get('selected_building_id').strip()

		sql="SELECT * FROM containers WHERE type='ROOM' AND (id=? OR name=?)"
		sql_p=[new_room_id,new_room_name]

		b = db_execute("readone",sql,sql_p)
		if b:
			html+="<p>ERROR: room name and id must be unique</p>"
		else:
			html+="<p>OK: room name and id are unique</p>"
			sql="INSERT INTO containers (id, type, container_id, name, status) VALUES (?,?,?,?,?)"
			sql_p=[new_room_id,"ROOM",selected_building_id,new_room_name,1]
			c=db_execute("write",sql,sql_p)
			html+="<p>OK: new room added</p>"
	else:
		sql="SELECT c1.id,(c1.name || ' (' || c1.id || ':' || c1.type || ')' ) AS name \
			FROM containers AS c1 \
			LEFT JOIN containers AS c2 ON c1.container_id=c2.id \
			WHERE c1.status=1 AND (c1.type='BUILDING') AND c1.container_id <> '' \
			ORDER BY c1.type, name"
		listBuildings = db_execute("readall",sql,"")
		html+=bottle.template('templates/add_room.tpl', listBuildings=listBuildings)

	html+=get_page_end()
	return(html)


##########################################################################################
@app.route('/add/shelves/')
@app.post('/add/shelves/')
def add_shelves():

	html=get_page_start()
	if bottle.request.POST.button_add_shelves:
		# Shelves Name and ID must be unique
		new_shelves_name = bottle.request.forms.get('new_shelves_name').strip()
		new_shelves_id = bottle.request.forms.get('new_shelves_id').strip()
		selected_room_id = bottle.request.forms.get('selected_room_id').strip()

		sql="SELECT * FROM containers WHERE type='SHELVES' AND (id=? OR name=?)"
		sql_p=[new_shelves_id,new_shelves_name]

		b = db_execute("readone",sql,sql_p)
		if b:
			html+="<p>ERROR: shelves name and id must be unique</p>"
		else:
			html+="<p>OK: shelves name and id are unique</p>"
			sql="INSERT INTO containers (id, type, container_id, name, status) VALUES (?,?,?,?,?)"
			sql_p=[new_shelves_id,"SHELVES",selected_room_id,new_shelves_name,1]
			c=db_execute("write",sql,sql_p)
			html+="<p>OK: new shelves added</p>"
	else:
		sql="SELECT c1.id,(c1.name || ' (' || c1.id || ':' || c1.type || ') @ ' || c2.name || '(' || c2.id ||')' ) AS name \
			FROM containers AS c1 \
			LEFT JOIN containers AS c2 ON c1.container_id=c2.id \
			WHERE c1.status=1 AND (c1.type='ROOM') AND c1.container_id <> '' \
			ORDER BY c1.type, name"
		listRooms = db_execute("readall",sql,"")
		html+=bottle.template('templates/add_shelves.tpl', listRooms=listRooms)

	html+=get_page_end()
	return(html)


##########################################################################################
@app.route('/add/shelf/')
@app.post('/add/shelf/')
def add_shelf():

	html=get_page_start()
	if bottle.request.POST.button_add_shelf:
		# Shelf Name and ID must be unique
		selected_shelves_id = bottle.request.forms.get('selected_shelves_id').strip()
		new_shelf_name = bottle.request.forms.get('new_shelf_name').strip()
		new_shelf_column = bottle.request.forms.get('new_shelf_column').strip()
		new_shelf_row = bottle.request.forms.get('new_shelf_row').strip()
		new_shelf_id = selected_shelves_id + "-" + new_shelf_column + new_shelf_row


		sql="SELECT * FROM containers WHERE type='SHELF' AND id=?"
		sql_p=[new_shelf_id,]

		b = db_execute("readone",sql,sql_p)
		if b:
			html+="<p>ERROR: shelf id must be unique</p>"
		else:
			html+="<p>OK: shelf id is unique</p>"
			sql="INSERT INTO containers (id, type, container_id, name, status) VALUES (?,?,?,?,?)"
			sql_p=[new_shelf_id,"SHELF",selected_shelves_id,new_shelf_name,1]
			c=db_execute("write",sql,sql_p)
			sql="INSERT INTO shelfs (id, column, row, type) VALUES (?,?,?,?)"
			sql_p=[new_shelf_id,new_shelf_column,new_shelf_row,"UNKNOWN"]
			c=db_execute("write",sql,sql_p)
			html+="<p>OK: new shelf added</p>"
	else:
		sql="SELECT c1.id,(c1.name || ' (' || c1.id || ':' || c1.type || ') @ ' || c2.name || '(' || c2.container_id || ':' || c2.type ||')' ) AS name \
			FROM containers AS c1 \
			LEFT JOIN containers AS c2 ON c1.container_id=c2.id \
			WHERE c1.status=1 AND (c1.type='SHELF' OR c1.type='ROOM') AND c1.container_id <> '' \
			ORDER BY c1.type, name"
		listShelves = db_execute("readall",sql,"")
		html+=bottle.template('templates/add_shelf.tpl', listShelves=listShelves)

	html+=get_page_end()
	return(html)


##########################################################################################
@app.route('/add/box/')
@app.post('/add/box/')
def add_box():

	html=get_page_start()
	if bottle.request.POST.button_add_box:
		# Shelf Name and ID must be unique
		new_box_name = bottle.request.forms.get('new_box_name').strip()
		new_box_id = bottle.request.forms.get('new_box_id').strip()
		selected_shelf_id = bottle.request.forms.get('selected_shelf_id').strip()

		sql="SELECT * FROM containers WHERE type='BOX' AND id=?"
		sql_p=[new_box_id,]

		b = db_execute("readone",sql,sql_p)
		if b:
			html+="<p>ERROR: box id must be unique</p>"
		else:
			html+="<p>OK: box id is unique</p>"
			sql="INSERT INTO containers (id, type, container_id, name, status) VALUES (?,?,?,?,?)"
			sql_p=[new_box_id,"BOX",selected_shelf_id,new_box_name,1]
			c=db_execute("write",sql,sql_p)
			html+="<p>OK: new box added</p>"
	else:
		sql="SELECT c1.id,(c1.name || ' (' || c1.id || ':' || c1.type || ') @ ' || c2.name || '(' || c2.container_id || ':' || c2.type ||')' ) AS name \
			FROM containers AS c1 \
			LEFT JOIN containers AS c2 ON c1.container_id=c2.id \
			WHERE c1.status=1 AND (c1.type='SHELF' OR c1.type='ROOM') AND c1.container_id <> '' \
			ORDER BY c1.type, name"
		listShelfs = db_execute("readall",sql,"")
		html+=bottle.template('templates/add_box.tpl', listShelfs=listShelfs)

	html+=get_page_end()
	return(html)


##########################################################################################
@app.route('/add/item/')
@app.post('/add/item/')
def add_item():

	html=get_page_start()
	if bottle.request.POST.button_add_item:
		# Item ID must be unique
		new_item_name = bottle.request.forms.get('new_item_name').strip()
		new_item_id = bottle.request.forms.get('new_item_id').strip()
		selected_container_id = bottle.request.forms.get('selected_container_id').strip()

		sql="SELECT * FROM items WHERE id=?"
		sql_p=[new_item_id,]

		b = db_execute("readone",sql,sql_p)
		if b:
			html+="<p>ERROR: item id must be unique</p>"
		else:
			html+="<p>OK: item id is unique</p>"
			sql="INSERT INTO items (id, container_id, name, status) VALUES (?,?,?,?)"
			sql_p=[new_item_id,selected_container_id,new_item_name,1]
			c=db_execute("write",sql,sql_p)
			html+="<p>OK: new item added</p>"
	else:
		sql="SELECT c1.id,(c1.name || ' (' || c1.id || ':' || c1.type || ') @ ' || c2.name || '(' || c2.container_id || ':' || c2.type ||')' ) AS name \
			FROM containers AS c1 \
			LEFT JOIN containers AS c2 ON c1.container_id=c2.id \
			WHERE c1.status=1 AND (c1.type='SHELVES' OR c1.type='SHELF' OR c1.type='ROOM') AND c1.container_id <> '' \
			ORDER BY c1.type, name"
		listContainers = db_execute("readall",sql,"")
		html+=bottle.template('templates/add_item.tpl', listContainers=listContainers)

	html+=get_page_end()
	return(html)


##########################################################################################
@app.route('/delete/container/')
@app.post('/delete/container/')
def delete_container():

	html=get_page_start()
	if bottle.request.POST.button_delete_container:
		confirmation = bottle.request.forms.get('confirmation_to_delete').strip()
		selected_container_id = bottle.request.forms.get('selected_container_id').strip()

		sql="SELECT * FROM containers WHERE container_id=? AND status=1"
		sql_p=[selected_container_id,]
		if confirmation==selected_container_id:
			b = db_execute("readone",sql,sql_p)
			if b:
				html+="<p>ERROR: can't delete container in use</p>"
			else:
				html+="<p>OK: container not is use</p>"
				sql="UPDATE containers SET status=0 WHERE id = ?"
				sql_p=[selected_container_id,]
				c=db_execute("write",sql,sql_p)
				html+="<p>OK: container is deleted</p>"
		else:
			html+="<p>ERROR: confirmation to delete not given</p>"
	else:
		sql="SELECT c1.id,(c1.name || ' (' || c1.id || ':' || c1.type || ') @ ' || c2.name || '(' || c2.container_id || ':' || c2.type ||')' ) AS name \
			FROM containers AS c1 \
			LEFT JOIN containers AS c2 ON c1.container_id=c2.id \
			WHERE c1.status=1 AND c1.container_id <> '' \
			ORDER BY c1.type, name"
		listContainers = db_execute("readall",sql,"")
		html+=bottle.template('templates/delete_container.tpl', listContainers=listContainers)

	html+=get_page_end()
	return(html)


##########################################################################################
@app.route('/delete/item/')
@app.post('/delete/item/')
def delete_item():

	html=get_page_start()
	if bottle.request.POST.button_delete_item:
		confirmation = bottle.request.forms.get('confirmation_to_delete').strip()
		selected_item_id = bottle.request.forms.get('selected_item_id').strip()

		if confirmation==selected_item_id:
			sql="UPDATE items SET status=0 WHERE id = ?"
			sql_p=[selected_item_id,]
			c=db_execute("write",sql,sql_p)
			html+="<p>OK: item is deleted</p>"
		else:
			html+="<p>ERROR: confirmation to delete not given</p>"
	else:
		sql="SELECT i.id, ( i.id || '@' || c.id || ' (' || i.name || '@' || c.name || ')' ) AS name \
			FROM items AS i \
			LEFT JOIN containers AS c ON i.container_id=c.id \
			WHERE i.status=1 AND c.container_id <> '' \
			ORDER BY i.name"
		listItems = db_execute("readall",sql,"")
		html+=bottle.template('templates/delete_item.tpl', listItems=listItems)

	html+=get_page_end()
	return(html)


##########################################################################################
@app.route('/modify/item_attributes/<modifyItemID>')
@app.post('/modify/item_attributes/<modifyItemID>')
def modify_item_attributes(modifyItemID):

	html=get_page_start()
	if bottle.request.POST.button_modify_item_attributes:
		newItemContainerID = bottle.request.forms.get('new_container_id').strip()
		newItemID = bottle.request.forms.get('new_item_id').strip()
		newItemName = bottle.request.forms.get('new_item_name').strip()

		sql="SELECT * FROM items WHERE id=?"
		sql_p=[modifyItemID,]
		itemAttributes = db_execute("readone",sql,sql_p)
		oldItemName=itemAttributes["name"]
		oldItemContainerID=itemAttributes["container_id"]


		#Check that possible new item ID is not in use
		if newItemID != modifyItemID:
			sql="SELECT * FROM items WHERE id = ?"
			sql_p=[newItemID]
			c=db_execute("readone",sql,sql_p)
			if not c:
				html+="<p>OK: new item ID is free</p>"			
				newItemIDOk=True
			else:
				html+="<p>ERROR: new item ID is NOT free</p>"	
				newItemIDOk=False
		else:
			newItemIDOk=True
				
		# Update name
		if newItemIDOk:
			if newItemName != oldItemName:
				sql="UPDATE items SET name=? WHERE id = ?"
				sql_p=[newItemName,modifyItemID]
				c=db_execute("write",sql,sql_p)
				html+="<p>OK: item name is updated - "+oldItemName+" -> "+newItemName+"</p>"
			# Update container id
			if newItemContainerID != oldItemContainerID:
				sql="UPDATE items SET container_id=? WHERE id = ?"
				sql_p=[newItemContainerID,modifyItemID]
				c=db_execute("write",sql,sql_p)
				html+="<p>OK: item container is updated - "+oldItemContainerID+" -> "+newItemContainerID+"</p>"
			# Update item id - THIS MUST BE LAST UPDATE!
			if newItemID != modifyItemID:
				sql="UPDATE items SET id=? WHERE id = ?"
				sql_p=[newItemID,modifyItemID]
				c=db_execute("write",sql,sql_p)
				html+="<p>OK: item id is updated - "+modifyItemID+" -> "+newItemID+"</p>"

		html+='<p><font color="RED">References to possible pictures, tags, triggers etc where not updated!</font></p>'

	else:
		sql="SELECT c1.id,(c1.name || ' (' || c1.id || ':' || c1.type || ') @ ' || c2.name || '(' || c2.container_id || ':' || c2.type ||')' ) AS name \
			FROM containers AS c1 \
			LEFT JOIN containers AS c2 ON c1.container_id=c2.id \
			WHERE c1.status=1 AND c1.container_id <> '' \
			ORDER BY c1.type, name"
		listContainers = db_execute("readall",sql,"")

		sql="SELECT * FROM items WHERE id=?"
		sql_p=[modifyItemID,]
		itemAttributes = db_execute("readone",sql,sql_p)
		modifyItemName=itemAttributes["name"]
		modifyItemContainerID=itemAttributes["container_id"]

		html+=bottle.template('templates/modify_item_attributes.tpl',   modifyItemID=modifyItemID, \
																		modifyItemName=modifyItemName, \
																		modifyItemContainerID=modifyItemContainerID, \
																		listContainers=listContainers)

	html+=get_page_end()
	return(html)


##########################################################################################
@app.route('/modify/container_attributes/<modifyContainerID>')
@app.post('/modify/container_attributes/<modifyContainerID>')
def modify_container_attributes(modifyContainerID):

	html=get_page_start()
	if bottle.request.POST.button_modify_container_attributes:
		newContainerID = bottle.request.forms.get('new_container_id').strip()
		newContainerName = bottle.request.forms.get('new_container_name').strip()
		newContainerContainerID = bottle.request.forms.get('new_container_container_id').strip()
		newContainerType = bottle.request.forms.get('new_container_type').strip()

		sql="SELECT * FROM containers WHERE id=?"
		sql_p=[modifyContainerID,]
		containerAttributes = db_execute("readone",sql,sql_p)
		oldContainerName=containerAttributes["name"]
		oldContainerContainerID=containerAttributes["container_id"]
		oldContainerType=containerAttributes["type"]

		# Update name
		if newContainerName != oldContainerName:
			sql="UPDATE containers SET name=? WHERE id = ?"
			sql_p=[newContainerName,modifyContainerID]
			c=db_execute("write",sql,sql_p)
			html+="<p>OK: container name is updated - "+oldContainerName+" -> "+newContainerName+"</p>"
		# Update container container id
		if newContainerContainerID != oldContainerContainerID:
			sql="UPDATE containers SET container_id=? WHERE id = ?"
			sql_p=[newContainerContainerID,modifyContainerID]
			c=db_execute("write",sql,sql_p)
			html+="<p>OK: container container is updated - "+oldContainerContainerID+" -> "+newContainerContainerID+"</p>"
		# Update container type
		if newContainerType != oldContainerType:
			sql="UPDATE containers SET type=? WHERE id = ?"
			sql_p=[newContainerType,modifyContainerID]
			c=db_execute("write",sql,sql_p)
			html+="<p>OK: container type is updated - "+oldContainerType+" -> "+newContainerType+"</p>"
		# Update container id - THIS MUST BE LAST UPDATE!
		if newContainerID != modifyContainerID:
			sql="UPDATE items SET container_id=? WHERE container_id = ?"
			sql_p=[newContainerID,modifyContainerID]
			c=db_execute("write",sql,sql_p)
			html+="<p>OK: item's container ids are updated - "+modifyContainerID+" -> "+newContainerID+"</p>"

			sql="UPDATE containers SET container_id=? WHERE container_id = ?"
			sql_p=[newContainerID,modifyContainerID]
			c=db_execute("write",sql,sql_p)
			html+="<p>OK: container's container ids are updated - "+modifyContainerID+" -> "+newContainerID+"</p>"

			sql="UPDATE containers SET id=? WHERE id = ?"
			sql_p=[newContainerID,modifyContainerID]
			c=db_execute("write",sql,sql_p)
			html+="<p>OK: container id is updated - "+modifyContainerID+" -> "+newContainerID+"</p>"

		html+='<p><font color="RED">References to possible pictures, tags, triggers etc where not updated!</font></p>'

	else:
		sql="SELECT * FROM containers WHERE id=?"
		sql_p=[modifyContainerID,]
		containerAttributes = db_execute("readone",sql,sql_p)
		modifyContainerName=containerAttributes["name"]
		modifyContainerContainerID=containerAttributes["container_id"]
		modifyContainerType=containerAttributes["type"]

		sql="SELECT c1.id,(c1.name || ' (' || c1.id || ':' || c1.type || ') @ ' || c2.name || '(' || c2.container_id || ':' || c2.type ||')' ) AS name \
			FROM containers AS c1 \
			LEFT JOIN containers AS c2 ON c1.container_id=c2.id \
			WHERE c1.status=1 AND c1.container_id <> '' \
			UNION \
			SELECT id, name FROM containers WHERE id='WORLD' \
			ORDER BY name \
			"
		listContainers = db_execute("readall",sql,"")


		html+=bottle.template('templates/modify_container_attributes.tpl',   modifyContainerID=modifyContainerID, \
																		modifyContainerName=modifyContainerName, \
																		modifyContainerContainerID=modifyContainerContainerID, \
																		modifyContainerType=modifyContainerType, \
																		listContainers=listContainers)
	html+=get_page_end()
	return(html)


##########################################################################################
@app.route('/annotations/list/')
@app.post('/annotations/list/')
def annotations_list():
	html=get_page_start()

	sql="SELECT id,type,list_id,text,status FROM annotations"
	sql_p=[]
	listAnnotations=db_execute("readall",sql,"")

	sql="SELECT id FROM annotation_lists GROUP BY id"
	sql_p=[]
	listAnnotationLists=db_execute("readall",sql,"")
	
	html+=bottle.template('templates/annotations_list.tpl', listAnnotations=listAnnotations,listAnnotationLists=listAnnotationLists)
	html+=get_page_end()
	return(html)


##########################################################################################
@app.route('/annotations/edit/<editAnnotationID>')
@app.post('/annotations/edit/<editAnnotationID>')
def annotations_delete(editAnnotationID):

	html=get_page_start()
	if bottle.request.POST.button_annotation_edit_start:
		sql="SELECT id,type,list_id,text,status FROM annotations WHERE id=?"
		sql_p=[editAnnotationID,]
		anno=db_execute("readone",sql, sql_p)
		editAnnotationID = anno["id"]
		editAnnotationType = anno["type"]
		editAnnotationListID = anno["list_id"]
		editAnnotationText = anno["text"]
		editAnnotationStatus = anno["status"]

		sql="SELECT id FROM annotation_lists GROUP BY id"
		listAnnoListIDs=[]
		listAnnoListIDs=db_execute("readall",sql, "")

		html+=bottle.template('templates/annotations_edit.tpl', \
								editAnnotationID=editAnnotationID, \
								editAnnotationType=editAnnotationType, \
								editAnnotationListID=editAnnotationListID, \
								editAnnotationText=editAnnotationText, \
								editAnnotationStatus=editAnnotationStatus, \
								listAnnoListIDs=listAnnoListIDs )

	elif bottle.request.POST.button_annotation_edit_save:
		editAnnotationID = bottle.request.forms.get('new_annotation_id').strip()
		editAnnotationType = bottle.request.forms.get('new_annotation_type').strip()
		editAnnotationListID = bottle.request.forms.get('new_annotation_list_id').strip()
		editAnnotationText = bottle.request.forms.get('new_annotation_text').strip()
		editAnnotationStatus = bottle.request.forms.get('new_annotation_status').strip()

		sql="UPDATE annotations SET type=?, list_id=?, text=?, status=? WHERE id=?"
		sql_p=[editAnnotationType,editAnnotationListID,editAnnotationText,editAnnotationStatus,editAnnotationID]
		c=db_execute("write",sql,sql_p)

		html+=bottle.template('templates/annotations_edit_save.tpl', \
								editAnnotationID=editAnnotationID, \
								editAnnotationType=editAnnotationType, \
								editAnnotationListID=editAnnotationListID, \
								editAnnotationText=editAnnotationText, \
								editAnnotationStatus=editAnnotationStatus )
	else:
		bottle.redirect('/annotations/list/')

	html+=get_page_end()
	return(html)


##########################################################################################
@app.route('/annotations/add/')
@app.post('/annotations/add/')
def annotations_add():

	html=get_page_start()
	if bottle.request.POST.button_add_new_annotation:
		newAnnotationType = bottle.request.forms.get('new_annotation_type').strip()
		newAnnotationListID = bottle.request.forms.get('new_annotation_list_id').strip()
		newAnnotationListIDCreate = bottle.request.forms.get('new_annotation_list_id_create').strip()
		newAnnotationText = bottle.request.forms.get('new_annotation_text').strip()
		newAnnotationStatus = bottle.request.forms.get('new_annotation_status').strip()

		sql="INSERT INTO annotations (id,type,list_id,text,status) VALUES ((SELECT MAX(id)+1 FROM annotations),?,?,?,?)"
		if newAnnotationListID == "_CREATE_NEW_":
			newAnnotationListID = newAnnotationListIDCreate
			
		sql_p=[newAnnotationType,newAnnotationListID,newAnnotationText,newAnnotationStatus]
		c=db_execute("write",sql,sql_p)

		bottle.redirect('/annotations/list/')

	html+=get_page_end()
	return(html)


##########################################################################################
@app.route('/annotations/delete/<deleteAnnotationID>')
@app.post('/annotations/delete/<deleteAnnotationID>')
def annotations_delete(deleteAnnotationID):

	html=get_page_start()
	if bottle.request.POST.button_annotation_delete_start:

		sql="SELECT * FROM item_annotations WHERE annotation_id = ?"
		sql_p=[deleteAnnotationID,]
		c=db_execute("readone",sql,sql_p)

		sql="SELECT id,type,list_id,text,status FROM annotations WHERE id=?"
		sql_p=[deleteAnnotationID,]
		anno=db_execute("readone",sql, sql_p)
		deleteAnnotationID = anno["id"]
		deleteAnnotationType = anno["type"]
		deleteAnnotationListID = anno["list_id"]
		deleteAnnotationText = anno["text"]
		deleteAnnotationStatus = anno["status"]

		if not c or len(c)==0:
			html+="<p>Annotation can be deleted</p>"
			html+=bottle.template('templates/annotations_delete.tpl', deleteAnnotationID = deleteAnnotationID, \
																	 deleteAnnotationType=deleteAnnotationType, \
																	 deleteAnnotationListID=deleteAnnotationListID, \
																	 deleteAnnotationText=deleteAnnotationText, \
																	 deleteAnnotationStatus=deleteAnnotationStatus )
		else:
			html+="<p>Found %s items using annotation ID %s. Annotation can't be deleted!" % (len(c),deleteAnnotationID)

	elif bottle.request.POST.button_annotation_delete_confirm:
		sql="SELECT * FROM item_annotations WHERE annotation_id = ?"
		sql_p=[deleteAnnotationID,]
		c=db_execute("readone",sql,sql_p)
		if not c or len(c)==0:
			sql="DELETE FROM annotations WHERE id = ?"
			d=db_execute("write",sql,sql_p)
			html+="<p>Annotation ID %s deleted</p>" % (deleteAnnotationID)
		else:
			html+="<p>Annotation ID %s can't be delete. Updated?</p>" % (deleteAnnotationID)

	elif bottle.request.POST.button_annotation_delete_cancel:
		bottle.redirect('/annotations/list/')
	else:
		bottle.redirect('/annotations/list/')

	html+=get_page_end()
	return(html)
	

##########################################################################################
@app.route('/annotation_lists/list/')
@app.post('/annotation_lists/list/')
def annotation_lists_list():
	html=get_page_start()

	sql="SELECT id,item FROM annotation_lists ORDER BY id,item"
	sql_p=[]
	listAnnotationListItems=db_execute("readall",sql,"")

	sql="SELECT list_id FROM annotations WHERE list_id != '' GROUP BY list_id ORDER BY list_id"
	sql_p=[]
	listAnnotationLists=db_execute("readall",sql,"")


	html+=bottle.template('templates/annotationlists_list.tpl', listAnnotationListItems=listAnnotationListItems,listAnnotationLists=listAnnotationLists)

	html+=get_page_end()
	return(html)

##########################################################################################
@app.route('/annotation_list_item/add/')
@app.post('/annotation_list_item/add/')
def annotation_lists_add():
	html=get_page_start()
	
	if bottle.request.POST.button_annotationlist_item_add:
		newAnnoListId = bottle.request.forms.get('new_annotation_list_id').strip()
		newAnnoListItem = bottle.request.forms.get('new_annotationlist_item_text').strip()

		sql="SELECT id,item FROM annotation_lists WHERE id=? AND item=?"
		sql_p=[newAnnoListId,newAnnoListItem]
		c=db_execute("readall",sql,sql_p)
		
		if c:
			html+="<p>Duplicate annotation list item</p>"
		elif newAnnoListId=="":
			html+="<p>Annotation list ID missing</p>"
		elif newAnnoListItem=="":
			html+="<p>Annotation list item missing</p>"
		else:
			sql="INSERT INTO annotation_lists (id, item) VALUES (?,?)"
			sql_p=[newAnnoListId,newAnnoListItem]
			c=db_execute("write",sql,sql_p)
			html+="<p>New annotation list item added</p>"
			bottle.redirect('/annotation_lists/list/')
			

	html+=get_page_end()
	return(html)


##########################################################################################
@app.post('/annotation_list_item/delete/')
@app.route('/annotation_list_item/delete/')
def annotation_list_item_delete():
	html=get_page_start()

	
	queryListID = bottle.request.query.delete_listID
	queryItemID = bottle.request.query.delete_itemID
	html+="<p>listID='%s' itemID='%s'</p>" % (queryListID,queryItemID)
	
	if bottle.request.POST.button_annotationlist_item_delete_start:
	
		sql='SELECT id,item FROM annotation_lists WHERE id=? AND item=?'
		sql_p=[queryListID,queryItemID]
		c=db_execute("readone",sql,sql_p)
		if not c:
			html+="<p>Annotation lists item %s %s doesn't exists</p>" % (queryListID,queryItemID)
		else:
			sql="SELECT * FROM item_annotations AS ia \
					LEFT JOIN annotations as a ON a.id=ia.annotation_id \
					WHERE a.type='LIST' AND a.list_id=? AND ia.value=?"
			sql_p=[queryListID,queryItemID]
			c=db_execute("readone",sql,sql_p)
			if c:
				html+="<p>Annotation lists item is in use. Can't delete!</p>"
			else:
				html+="<p>Annotation lists item deleted.</p>"
				sql="DELETE FROM annotation_lists WHERE id=? AND item=?"
				sql_p=[queryListID,queryItemID]
				c=db_execute("write",sql,sql_p)
				
				bottle.redirect('/annotation_lists/list/')
	else:
		html+="<p>Ooho sanoi Lari! change this to use queries in url</p>"
				
				
	
	
	html+=get_page_end()
	return(html)


##########################################################################################
@app.route('/annotation/add/<editItemID>')
@app.post('/annotation/add/<editItemID>')
def annotations_item_add(editItemID):

	html=get_page_start()
	if bottle.request.POST.button_annotation_add_save:
		html+="<p>Selected annotations for adding</p>"
		annoSelected = bottle.request.forms.getlist('annotation_selected')
		
		for a in annoSelected:
			annoValue = bottle.request.forms.get('annotation_value_%s' % a)
			html+="<p>Add annotation ID '%s' with value '%s' for item '%s'</p>" % (a, annoValue, editItemID)
			sql="INSERT INTO item_annotations (item_id,annotation_id,value) VALUES (?,?,?)"
			sql_p=[editItemID,a,annoValue]
			c=db_execute("write",sql,sql_p)
		html+="<p>All annotations added</p>"
			
	else:
		sql="SELECT a.id, a.type, a.list_id, a.text, a.status, a.timestamp \
			FROM annotations AS a \
			LEFT OUTER JOIN item_annotations AS ia ON a.id = ia.annotation_id AND ia.item_id = ? \
			WHERE ia.item_id IS Null "
			
		sql_p=[editItemID,]
		listAnnotations=db_execute("readall",sql,sql_p)
		
		sql="SELECT id,item FROM annotation_lists ORDER BY id,item"
		sql_p=[]
		listAnnotationListItems=db_execute("readall",sql,"")

		html+=bottle.template('templates/annotation_item_add.tpl', editItemID=editItemID, \
															listAnnotations=listAnnotations, \
															listAnnotationListItems=listAnnotationListItems )


	

	html+=get_page_end()
	return(html)

##########################################################################################
@app.route('/annotation/modify/<editItemID>')
@app.post('/annotation/modify/<editItemID>')
def annotations_item_modify(editItemID):

	html=get_page_start()
	if bottle.request.POST.button_annotation_modify_save:

		
		sql="SELECT annotation_id, value FROM item_annotations WHERE item_id = ?"
		sql_p=[editItemID,]
		itemAnno=db_execute("readall",sql,sql_p)
		
		for a in itemAnno:
			annoValue = bottle.request.forms.get('annotation_value_%s' % a[0])
			if a[1] != annoValue:
				html+="<p>New annotation value '%s' -> '%s' for annotation id %s for item %s</p>" % (a[1],annoValue,a[0],editItemID)
				sql="UPDATE item_annotations SET value=? WHERE item_id=? and annotation_id=?"
				sql_p=[annoValue,editItemID,a[0]]
				c=db_execute("write",sql,sql_p)

		html+="<p>Annotation changes saved</p>"
			
	else:
		sql="SELECT ia.item_id, ia.annotation_id, ia.value, a.type, a.list_id, a.text, a.status \
			FROM item_annotations AS ia \
			LEFT JOIN annotations AS a ON a.id = ia.annotation_id \
			WHERE ia.item_id=? \
			ORDER BY a.text"
			
		sql_p=[editItemID,]
		itemAnnotations=db_execute("readall",sql,sql_p)
		
		sql="SELECT id,item FROM annotation_lists ORDER BY id,item"
		listAnnotationListItems=db_execute("readall",sql,"")

		html+=bottle.template('templates/annotation_item_modify.tpl', editItemID=editItemID, \
															itemAnnotations=itemAnnotations, \
															listAnnotationListItems=listAnnotationListItems )


	

	html+=get_page_end()
	return(html)


##########################################################################################
@app.route('/world/')
@app.route('/world/<selectedBuilding>/')
@app.route('/world/<selectedBuilding>/<selectedRoom>/')
@app.route('/world/<selectedBuilding>/<selectedRoom>/<selectedObjectLevel1>/')
@app.route('/world/<selectedBuilding>/<selectedRoom>/<selectedObjectLevel1>/<selectedObjectLevel2>/')
@app.route('/world/<selectedBuilding>/<selectedRoom>/<selectedObjectLevel1>/<selectedObjectLevel2>/<selectedObjectLevel3>/')
@app.route('/world/<selectedBuilding>/<selectedRoom>/<selectedObjectLevel1>/<selectedObjectLevel2>/<selectedObjectLevel3>/<selectedObjectLevel4>/')
def world(selectedBuilding="",selectedRoom="",selectedObjectLevel1="",selectedObjectLevel2="",selectedObjectLevel3="", selectedObjectLevel4=""):

	html=get_page_start()

	sql_base="SELECT id, type, container_id, name FROM containers "

	listItems=[]
	listLevel1Objects = None
	listLevel2Objects = None
	listLevel3Objects = None
	listLevel4Objects = None
	lastSelectedObject = None

	# List of all buildings
	sql = sql_base + "WHERE status=1 AND container_id='WORLD' ORDER BY id"
	listBuildings = db_execute("readall",sql,"")

	# List of all rooms of selected building
	if selectedBuilding=="":
		listRooms = None
		listItems=get_all_items("WORLD")
	else:
		sql = sql_base + "WHERE status=1 AND container_id='%s' ORDER BY id" % selectedBuilding
		listRooms = db_execute("readall",sql,"")
		lastSelectedObject = selectedBuilding

		# List of level 1 objects
		if selectedRoom=="":
			listItems=get_all_items(selectedBuilding)
		else:
			sql = sql_base + "WHERE status=1 AND container_id='%s' ORDER BY id" % selectedRoom
			listLevel1Objects = db_execute("readall",sql,"")
			lastSelectedObject = selectedRoom

			# List of level 2 objects
			if selectedObjectLevel1=="":
				listItems=get_all_items(selectedRoom)
			else:
				sql = sql_base + "WHERE status=1 AND container_id='%s' ORDER BY id" % selectedObjectLevel1
				listLevel2Objects = db_execute("readall",sql,"")
				lastSelectedObject = selectedObjectLevel1

				# List of level 3 objects
				if selectedObjectLevel2=="":
					listItems=get_all_items(selectedObjectLevel1)
				else:
					sql = sql_base + "WHERE status=1 AND container_id='%s' ORDER BY id" % selectedObjectLevel2
					listLevel3Objects = db_execute("readall",sql,"")
					lastSelectedObject = selectedObjectLevel2

					# List of level 4 objects
					if selectedObjectLevel3=="":
						listItems=get_all_items(selectedObjectLevel2)
					else:
						sql = sql_base + "WHERE status=1 AND container_id='%s' ORDER BY id" % selectedObjectLevel3
						listLevel4Objects = db_execute("readall",sql,"")
						listItems=get_all_items(selectedObjectLevel3)
						lastSelectedObject = selectedObjectLevel3

	querySelectedItemID = bottle.request.query.selected_item_id
	if querySelectedItemID:
		sql="SELECT id, container_id, name, status, timestamp FROM items WHERE id=?"
		sql_p=[querySelectedItemID,]
		item=db_execute("readone",sql,sql_p)
		selectedItemInfo=[]
		selectedItemInfo.append(["ID",item["id"]])
		selectedItemInfo.append(["Container ID",item["container_id"]])
		selectedItemInfo.append(["Name",item["name"]])
		selectedItemInfo.append(["Status",item["status"]])
		selectedItemInfo.append(["Timestamp",item["timestamp"]])

		sql="SELECT ia.item_id, ia.annotation_id, ia.value AS value, ia.timestamp, anno.text AS text FROM item_annotations AS ia \
			LEFT JOIN annotations AS anno ON anno.id = ia.annotation_id \
			WHERE ia.item_id=? \
			ORDER BY anno.text"

		sql_p=[querySelectedItemID,]
		anno=db_execute("readall",sql,sql_p)
		selectedItemAnnotations=[]
		for a in anno:
			selectedItemAnnotations.append([a["text"],a["value"]])

	else:
		selectedItemInfo=[]
		selectedItemAnnotations=[]

	pageURL = bottle.request.fullpath

	html+=bottle.template('templates/world.tpl',selectedBuilding=selectedBuilding, \
												selectedRoom=selectedRoom, \
												selectedObjectLevel1=selectedObjectLevel1, \
												selectedObjectLevel2=selectedObjectLevel2, \
												selectedObjectLevel3=selectedObjectLevel3, \
												selectedObjectLevel4=selectedObjectLevel4, \
												listBuildings=listBuildings, \
												listRooms=listRooms, \
												listLevel1Objects=listLevel1Objects, \
												listLevel2Objects=listLevel2Objects, \
												listLevel3Objects=listLevel3Objects, \
												listLevel4Objects=listLevel4Objects, \
												listItems=listItems, \
												lastSelectedObject = lastSelectedObject, \
												selectedItemInfo = selectedItemInfo, \
												querySelectedItemID = querySelectedItemID, \
												selectedItemAnnotations = selectedItemAnnotations, \
												pageURL = pageURL )

	html+="<p>Items: %s</p>" % (len(listItems))
	html+="<p>URL: %s</p>" %  (bottle.request.url)
	#for i in listItems:
	#	html+="<p>a%s</p>" % i

	html+=get_page_end()
	return (html)


##########################################################################################
if __name__=='__main__':
	bottle.debug(True) # Comment this row out for production use
	bottle.run(app=app,host='localhost',port=80,reloader=True)
