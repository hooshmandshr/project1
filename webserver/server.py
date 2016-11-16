#!/usr/bin/env python2.7

"""
Columbia W4111 Intro to databases
Example webserver

To run locally

    python server.py

Go to http://localhost:8111 in your browser


A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""

import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response, url_for, jsonify, json, session

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)
app._static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

import datetime as dt

#
# The following uses the postgresql test.db -- you can use this for debugging purposes
# However for the project you will need to connect to your Part 2 database in order to use the
# data
#
# XXX: The URI should be in the format of: 
#
#     postgresql://USER:PASSWORD@<IP_OF_POSTGRE_SQL_SERVER>/postgres
#
# For example, if you had username ewu2493, password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://ewu2493:foobar@<IP_OF_POSTGRE_SQL_SERVER>/postgres"
#
# Swap out the URI below with the URI for the database created in part 2
DATABASEURI = "postgresql://hs2703:q5sk7@104.196.175.120/postgres"


#
# This line creates a database engine that knows how to connect to the URI above
#
engine = create_engine(DATABASEURI)


@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request

  The variable g is globally accessible
  """
  try:
    g.conn = engine.connect()
  except:
    print "uh oh, problem connecting to database"
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't the database could run out of memory!
  """
  try:
    g.conn.close()
    print "successfully closed connection to database."
  except Exception as e:
    pass


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to e.g., localhost:8111/foobar/ with POST or GET then you could use
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
# 
# see for routing: http://flask.pocoo.org/docs/0.10/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
@app.route('/')
def index():
  """
  request is a special object that Flask provides to access web request information:

  request.method:   "GET" or "POST"
  request.form:     if the browser submitted a form, this contains the data in the form
  request.args:     dictionary of URL arguments e.g., {a:1, b:2} for http://localhost?a=1&b=2

  See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
  """
  
  # Redirect to login page as home page
  return redirect(url_for("login"))
  
@app.route("/login")
def login():
	return render_template("login.html", header2='')
	
@app.route("/authentication", methods=['POST'])
def authentication():
  
	# DEBUG: this is debugging code to see what request looks like
	print request.args
	# pass real data here
	username=request.form["username"]
	password=request.form["password"]
	
	cursor = g.conn.execute("SELECT * FROM users WHERE users.username=%s", username)
	result = cursor.first()
	cursor.close()
	
	if result == None or result['password'] != password:
		return render_template("login.html", headerError='Invalid username or password')
	else:
		session['username'] = username
		session['firstname'] = result['firstname']
		if result['usertype'] == 'regular':
			return redirect(url_for("eventplanner"))
		else:
			return redirect(url_for("venueowner"))
  #     {% for n in data %}
  #     <div>{{n}}</div>
  #     {% endfor %}
  #
@app.route("/register", methods=['POST'])
def register():
	return render_template("register.html", headerError='')

@app.route("/createuser", methods=['POST'])
def createuser():
	username=request.form["username"]
	firstname=request.form["firstname"]
	lastname=request.form["lastname"]
	password=request.form["password"]
	dob=request.form["dob"]
	gender=request.form["gender"]
	address=request.form["address"]
	email=request.form["email"]
	phone=request.form["phone"]
	usertype=request.form["usertype"]
	#check whether username availables
	cursor = g.conn.execute("SELECT * FROM users WHERE users.username=%s", username)
	result = cursor.first()
	cursor.close()
	if result != None:
		return render_template("register.html", headerError='user name not available')
	#check whether email availables
	emailFlag = False
	cursor = g.conn.execute("SELECT * FROM users WHERE users.email=%s", email)
	result = cursor.first()
	cursor.close()
	if result != None:
		return render_template("register.html", headerError='email already registered')
	#check date format
	try:
		dt.datetime.strptime(dob, '%d/%m/%Y')
	except:
		return render_template("register.html", headerError='incorrect date of birth format')

	cursor = g.conn.execute('INSERT INTO  users' + \
							'(username, firstname, lastname, password, dob, gender, address, usertype, email, phone)' + \
							'VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);',
							username, firstname, lastname, password, dob, gender, address, usertype, email, phone)
	cursor.close()
	return redirect(url_for("login"))
  
#user
@app.route("/eventplanner", methods=['GET', 'POST'])
def eventplanner():
	#clear selected event session
	if session.get('eventid'):
		session.pop('eventid', None)
	username = session['username']
	firstname = session['firstname']
	cursor = g.conn.execute("select events.eid, events.title, events.description, events.budget " + \
							"from events, users " + \
							"where events.organizer=users.username and " + \
							"users.username=%s;", username)
	eventDict = {}
	for res in cursor:
		eid = res['eid']
		eventDict[eid]={}
		eventDict[eid]['title']=res['title']
		eventDict[eid]['description']=res['description']
		eventDict[eid]['organizer']=username
		eventDict[eid]['budget']=res['budget']
	cursor.close()
	session['eventDict'] = eventDict
	return render_template("eventplanner.html", name=firstname, events=eventDict)
	
@app.route("/venueowner", methods=['GET', 'POST'])
def venueowner():
	username = session['username']
	firstname = session['firstname']
	cursor = g.conn.execute("select venues.vid, venues.name, venues.address, venues.capacity, venues.facilities " + \
							"from venues, registrations, users " + \
							"where venues.vid=registrations.vid and " + \
							"users.username=registrations.username and users.username=%s;", username)
	venueDict = {}
	for res in cursor:
		vid = res['vid']
		venueDict[vid]={}
		venueDict[vid]['name']=res['name']
		venueDict[vid]['address']=res['address']
		venueDict[vid]['capacity']=res['capacity']
		venueDict[vid]['facility']=res['facilities']
		cursor2 = g.conn.execute("select t.datefrom, t.dateto, t.tsid from timeslots t where t.vid=%s;", vid);
		venueDict[vid]['timeslots']={}
		for result in cursor2:
			venueDict[vid]['timeslots'][result['tsid']] = {}
			venueDict[vid]['timeslots'][result['tsid']]['datefrom'] = result['datefrom']
			venueDict[vid]['timeslots'][result['tsid']]['dateto'] = result['dateto']
		cursor2.close()
		venueDict[vid]['request']={}
		#venueDict[vid]['request']['resid']=str(i)+'resid'
		#venueDict[vid]['request']['eventid']=str(i)+'eventid'
		#venueDict[vid]['request']['tsid']=str(i)+'tsid'
	#session["venueDict"] = venueDict
	cursor.close()
	return render_template("venueowner.html", name=firstname, venue=venueDict)	

#event
@app.route("/editevent", methods=['POST'])
def editevent():
	if request.form['editbutton']=='edit':
		cursor = g.conn.execute('update events ' + \
						'set title=%s, description=%s, budget=%s ' + \
						'where events.eid=%s',
						request.form["title"], request.form["description"], request.form["budget"], request.form["eid"])
		cursor.close()
	elif request.form['editbutton']=='delete':
		cursor = g.conn.execute('delete from events ' + \
								'where events.eid=%s;', request.form["eid"])
		cursor.close()
	cursor.close()
	return redirect(url_for("eventplanner"))

@app.route("/addevent", methods=['POST'])
def addevent():
	title=request.form["title"]
	description=request.form["description"]
	organizer=session['username']
	budget=request.form["budget"]
	# pass real data here
	cursor = g.conn.execute('select Max(events.eid) as eid from events;')
	result = cursor.first()
	#increment max id to get next available
	eid = int(result['eid']) + 1
	cursor.close()
	# add event to database
	cursor = g.conn.execute('INSERT INTO  events' + \
							'(eid, title, description, organizer, budget)' + \
							'VALUES(%s, %s, %s, %s, %s);',
							eid, title, description, organizer, budget)
	cursor.close()
	return redirect(url_for("eventplanner"))

@app.route("/invite",methods=['GET', 'POST'])
def invite():
	try:

		eid=request.form['selected_event']
		session['eventid'] = eid
	except:
		eid = session['eventid']
		#session.pop('eventid', None)
	cursor = g.conn.execute('select events.description, events.title from events where events.eid=%s;', eid)
	result = cursor.first()
	event_name = result['title']
	event_description = result['description']
	cursor.close()
	cursor = g.conn.execute('select * from invitations where invitations.eid=%s;', eid) 
	invite={}
	for result in cursor:
		invid = result['invid']
		invite[invid]={}
		invite[invid]['invid']=result['invid']
		invite[invid]['eid']=result['invid']
		invite[invid]['username']=result['username']
		invite[invid]['title']=result['title']
		invite[invid]['message']=result['message']
		invite[invid]['preference']=result['preferences']
		invite[invid]['attending']=result['attending']
	#populate the dictionary and pass real data here
	cursor.close()
	return render_template("invite.html", invite=invite ,eid=eid,
							event_description=event_description, event_name=event_name)


@app.route("/newinvite",methods=['POST'])
def newinvite():
	#eid=request.form['selected_event']
	#eid=request.form['evidn']
	eid = session['eventid']
	username=request.form['username']
	title=request.form['title']
	message=request.form['message']
	session['eventid'] = eid
	# find invitation id
	cursor = g.conn.execute('select MAX(invitations.invid) as max from invitations')
	# pass real data here
	result = cursor.first()
	invid = result['max']
	invid += 1
	cursor.close()
	print invid
	cursor = g.conn.execute('INSERT INTO  invitations' + \
							'(invid, eid, username, title, message)' + \
							'VALUES(%s, %s, %s, %s, %s);',
							invid, eid, username, title, message)
	cursor.close()
	return redirect(url_for("invite"))

@app.route("/editinvite",methods=['GET', 'POST'])
def editinvite():
	# pass real data here
	if request.form['editbutton']=='edit':
		cursor = g.conn.execute('update invitations ' + \
								'set title=%s, message=%s ' + \
								'where invitations.invid=%s;',
								request.form["title"], request.form["message"], request.form["invidn"])
		cursor.close()
	elif request.form['editbutton']=='delete':
		cursor = g.conn.execute('delete from invitations ' + \
								'where invitations.invid=%s;', request.form["invidn"])
		cursor.close()
	return redirect(url_for("invite"))

@app.route("/request",methods=['POST'])
def requests():	
	username=session['username']
	eid=request.form['selected_event']
	session['evvid'] = eid 
	
	cursor = g.conn.execute("with available as (select tsid from timeslots except select tsid from reservations) " + \
							"select t.dateto, t.datefrom, t.tsid, v.name, v.address, v.capacity, v.facilities " + \
							"from timeslots t, venues v, available a where t.vid=v.vid and a.tsid=t.tsid;");
	timeslots={}
	for result in cursor:
		tsid = result['tsid']
		timeslots[tsid]={}
		timeslots[tsid]['datefrom']=result['datefrom']
		timeslots[tsid]['dateto']=result['dateto']
		timeslots[tsid]['name']=result['name']
		timeslots[tsid]['capacity']=result['capacity']
		timeslots[tsid]['facilities']=result['facilities']
	cursor.close()
	
	cursor = g.conn.execute("select t.datefrom, t.dateto, v.name, v.capacity, v.facilities " + \
							"from reservations r, events e, timeslots t, venues v " + \
							"where r.eid=%s and e.eid=r.eid and t.tsid=r.tsid and v.vid=t.vid;",
							eid);
	result = cursor.first()
	cursor.close()
	stimeslot={}
	session['hasRes'] = False
	if result == None:	
		stimeslot['datefrom']=None
		stimeslot['dateto']=None
		stimeslot['name']=None
		stimeslot['capacity']=None
		stimeslot['facilities']=None
	else:
		session['hasRes'] = True
		stimeslot['datefrom']=result['datefrom']
		stimeslot['dateto']=result['dateto']
		stimeslot['name']=result['name']
		stimeslot['capacity']=result['capacity']
		stimeslot['facilities']=result['facilities']
	
	return render_template("timeslot.html",name=username,assigned=stimeslot,totalslot=timeslots, eid=eid)

@app.route("/requestnewtimeslot", methods=['GET', 'POST'])
def requestnewtimeslot():
	if request.form['actbutton']=='cancel':
		return redirect(url_for("eventplanner"))
	elif request.form['actbutton']=='reserve':
		tsid = request.form['newslot']
		eid = session['evvid']
		if session['hasRes']:
			cursor = g.conn.execute("update reservations " + \
									'set tsid=%s where  reservations.eid=%s', tsid, eid);
			cursor.close()
		else:
			cursor = g.conn.execute('select Max(reservations.resid) as resid from reservations;')
			result = cursor.first()
			# increment max id to get next available
			resid = int(result['resid']) + 1
			cursor.close()
			cursor = g.conn.execute("INSERT INTO reservations(resid,eid,tsid) VALUES " + \
									"(%s, %s, %s)", resid, eid, tsid);
		# pass real data here
	return redirect(url_for("eventplanner"))

@app.route("/inventory", methods=['GET', 'POST'])
def inventory():
	try:
		eid=request.form['selected_event']
		print eid
		session['eid'] = eid
	except:
		eid=session['eid']
	# get inventory for selected event
	cursor = g.conn.execute("select i.isid, s.barcode, ii.name as item, ss.name as suplier, s.price, i.quantity, i.memo " + \
							"from inventory i, itemsupliers s, items ii, supliers ss " + \
							"where eid=%s and i.isid=s.isid and ii.barcode=s.barcode and ss.sid=s.sid;", eid);
	inventory={}
	for result in cursor:
		isid = result['isid']
		inventory[isid]={}
		inventory[isid]['barcode'] = result['barcode']
		inventory[isid]['item'] = result['item']
		inventory[isid]['suplier'] = result['suplier']
		inventory[isid]['price'] = result['price']
		inventory[isid]['quantity'] = result['quantity']
		inventory[isid]['memo'] = result['memo']
	cursor.close()
	# get total available items
	cursor = g.conn.execute("select iss.isid, i.barcode, i.name as item, s.name as suplier, iss.price, iss.instock " + \
							"from itemsupliers iss, items i, supliers s " + \
							"where iss.barcode=i.barcode and s.sid=iss.sid;", eid);
	stocks={}
	for result in cursor:
		isid = result['isid']
		stocks[isid]={}
		stocks[isid]['barcode'] = result['barcode']
		stocks[isid]['item'] = result['item']
		stocks[isid]['suplier'] = result['suplier']
		stocks[isid]['price'] = result['price']
		stocks[isid]['instock'] = result['instock']
	cursor.close()
	# add inventory and stocks to session for /newitem
	session['inventory'] = inventory
	session['stocks'] = stocks
	return render_template("inventory.html",eid=eid,inventory=inventory, stocks=stocks)

@app.route("/newitem",methods=['POST'])
def newitem():
	eid = session['eid']
	inventory = session['inventory']
	stocks = session['stocks']
	print request.form
	# clear session eid and go back to eventplanner
	if request.form['action']=='cancel':
		session.pop('eid', None)
		session.pop('inventory', None)
		session.pop('stocks', None)
		return redirect(url_for("eventplanner"))
	# remove selected items from inventory
	elif request.form['action']=='remove':
		isid = request.form['removeitem']
		cursor = g.conn.execute('delete from inventory i ' + \
								'where i.eid=%s and i.isid=%s;', eid, isid)
		cursor.close()
	# add selected item to inventory
	elif request.form['action']=='add':
		isid = request.form['newitem']
		quantity = request.form['quantity']
		if isid in inventory:
			newquant = int(inventory[isid]['quantity'])+int(request.form['quantity'])
			cursor = g.conn.execute('update inventory ' + \
									'set quantity=%s, memo=%s ' + \
									'where inventory.eid=%s and inventory.isid=%s', 
									newquant, request.form['memo'], eid, isid);
			cursor.close()
		else:
			cursor = g.conn.execute('insert into inventory' + \
									'(eid,isid,quantity,memo) ' + \
									'VALUES(%s, %s, %s, %s);', 
									eid, isid, request.form['quantity'], request.form['memo']);
			cursor.close()
	return redirect(url_for("inventory"))	

#venue
@app.route("/registervenue", methods=['POST'])
def registervenue():
	username=session['username']
	name=request.form["name"]
	address=request.form["address"]
	capacity=request.form["capacity"]
	facility=request.form["facility"]
	# pass real data here
	cursor = g.conn.execute('select Max(venues.vid) as vid from venues;')
	result = cursor.first()
	# increment max id to get next available
	vid = int(result['vid']) + 1
	cursor.close()
	# add venue
	cursor = g.conn.execute('INSERT INTO venues(vid,name,address,capacity,facilities) '+ \
							'values(%s, %s, %s, %s, %s);', vid, name, address, capacity, facility)
	cursor.close()
	# add registration
	cursor = g.conn.execute('select Max(registrations.regid) as regid from registrations;')
	result = cursor.first()
	#increment max id to get next available
	regid = int(result['regid']) + 1
	cursor.close()
	cursor = g.conn.execute('INSERT INTO registrations(regid,vid,username,role) '+ \
							"values(%s, %s, %s, 'manager');", regid, vid, username)
	cursor.close()
	return redirect(url_for("venueowner"))

@app.route("/managevenue", methods=['POST'])
def managevenue():
	print request.form
	# pass real data here
	cursor = g.conn.execute('update venues ' + \
					'set name=%s, address=%s, capacity=%s, facilities=%s ' + \
					'where venues.vid=%s',
					request.form["vname"], request.form["address"], request.form["capacity"], request.form["facility"], request.form["vid"])
	cursor.close()
	return redirect(url_for("venueowner"))

@app.route("/addtimeslot", methods=['POST'])
def addtimeslot():
	if request.form['tsbutton']=="add":
		cursor = g.conn.execute('select Max(timeslots.tsid) as tsid from timeslots;')
		result = cursor.first()
		#increment max id to get next available
		tsid = int(result['tsid']) + 1
		cursor.close()
		vid = request.form['vid']
		# pass real data here
		cursor = g.conn.execute('INSERT INTO timeslots(tsid,vid,datefrom,dateto) '+ \
							"values(%s, %s, %s, %s);", tsid, vid, request.form['datefrom'], request.form['dateto'])
		cursor.close()
	elif request.form['tsbutton']=="rem":
		cursor = g.conn.execute('delete from timeslots where timeslots.tsid=%s;', request.form["removeslot"])
		cursor.close()
	return redirect(url_for("venueowner"))

@app.route("/reservation", methods=['POST'])
def reservation():
	if request.form['response'] == "confirm":
		username=request.form['username']
		# pass real data here
		venue=venueowner(username)
		return render_template("venueowner.html", name=username, venue=venue)
	if request.form['response'] == "decline":
		username=request.form['username']
		# pass real data here
		venue=venueowner(username)
		return render_template("venueowner.html", name=username, venue=venue)

#sign out	
@app.route("/signout",methods=['GET', 'POST'])
def signout():
	session.clear()
	return redirect(url_for("login"))


if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='localhost')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using

        python server.py

    Show the help text using

        python server.py --help

    """
	
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    HOST, PORT = host, port
    print "running on %s:%d" % (HOST, PORT)
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


  run()
