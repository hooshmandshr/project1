from flask import Flask, render_template, url_for, request, redirect, jsonify, json
app = Flask(__name__)


def venueowner(username):
	venue={}
	#use username and pass real data here
	for i in [1,2]:
		venue[i]={}
		venue[i]['name']=str(i)+'venue'
		venue[i]['address']=str(i)+'address'
		venue[i]['capacity']=str(i)+'capacity'
		venue[i]['facility']=str(i)+'facility'
		venue[i]['ts_from']=str(i)+'date from'
		venue[i]['ts_to']=str(i)+'date to'
		venue[i]['request']={}
		venue[i]['request']['resid']=str(i)+'resid'
		venue[i]['request']['eventid']=str(i)+'eventid'
		venue[i]['request']['tsid']=str(i)+'tsid'
	return venue

def eventplanner(username):
	event={}
	for i in [1,2]:
		event[i]={}
		event[i]['eid']=str(i)+'eid'
		event[i]['title']=str(i)+'title'
		event[i]['description']=str(i)+'description'
		event[i]['organizer']=username
		event[i]['budget']=str(i)+'budget'
	return event

def invitation(username,eid):
	invite={}
	for i in [1,2]:
		invite[i]={}
		invite[i]['invid']=str(i)+'invid'
		invite[i]['eid']=eid
		invite[i]['username']=username
		invite[i]['title']='title'
		invite[i]['message']='message'
		invite[i]['preference']='preference'
		invite[i]['attending']='attending'
	return invite


def singletimeslot(username,eid):
	timeslot={}
	timeslot['id']='id'
	timeslot['vid']='vid'
	timeslot['datefrom']='datefrom'
	timeslot['dateto']='dateto'
	return timeslot



def timeslotobj():
	timeslot={}
	for i in [1,2]:
		timeslot[i]={}
		timeslot[i]['id']='id'
		timeslot[i]['vid']='vid'
		timeslot[i]['datefrom']='datefrom'
		timeslot[i]['dateto']='dateto'
	return timeslot

def inventorylist(username,eid):
	inventory={}
	for i in [1,2]:
		inventory[i]={}
		inventory[i]['eid']=eid
		inventory[i]['quantity']='quantity'
		inventory[i]['memo']='memo'
	return inventory

def totalitem():
	stocks={}
	for i in [1,2]:
		stocks[i]={}
		stocks[i]['barcode']='barcode'
		stocks[i]['sid']='sid'
		stocks[i]['price']='price'
		stocks[i]['instock']='instock'
	return stocks







#login
@app.route("/")
def index():
	#return render_template("index.html", saysomething="hello")
	return redirect(url_for("login"))

@app.route("/login")
def login():
	return render_template("login.html")

@app.route("/authentication", methods=['POST'])
def authentication():
	# pass real data here
	username=request.form["username"]
	password=request.form["password"]
	if username == "lily" and password == "hello":
		event=eventplanner(username)
		return render_template("eventplanner.html", name=username, events=event)
	if username == "hooshmand" and password == "hello":
		venue=venueowner(username)
		return render_template("venueowner.html", name=username, venue=venue)
	return username






#event
@app.route("/editevent", methods=['POST'])
def editevent():
	username=request.form["username"]
	event=eventplanner(username)
	# pass real data here
	return render_template("eventplanner.html", name=username, events=event)

@app.route("/addevent", methods=['POST'])
def addevent():
	username=request.form["username"]
	eid=request.form["eid"]
	title=request.form["title"]
	description=request.form["description"]
	organizer=request.form["organizer"]
	budget=request.form["budget"]
	dresscode=request.form["dresscode"]
	sponsor=request.form["sponsor"]
	event=eventplanner(username)
	# pass real data here
	return render_template("eventplanner.html", name=username, events=event)

@app.route("/invite",methods=['POST'])
def invite():
	username=request.form['username']
	eid=request.form['selected_event']
	invites=invitation(username,eid)
	#populate the dictionary and pass real data here
	return render_template("invite.html", name=username,invite=invites,eid=eid)


@app.route("/newinvite",methods=['POST'])
def newinvite():
	username=request.form['username']
	eid=request.form['evidn']
	event=eventplanner(username)
	# pass real data here
	return render_template("eventplanner.html", name=username, events=event)

@app.route("/editinvite",methods=['POST'])
def editinvite():
	username=request.form['username']
	eid=request.form['evidn']
	event=eventplanner(username)
	# pass real data here
	return render_template("eventplanner.html", name=username, events=event)

@app.route("/request",methods=['POST'])
def requests():
	username=request.form['username']
	eid=request.form['selected_event']
	totaltimeslot=timeslotobj()
	assignedtimeslot=singletimeslot(username,eid)
	return render_template("timeslot.html",name=username,assigned=assignedtimeslot,totalslot=totaltimeslot, eid=eid)

@app.route("/requestnewtimeslot", methods=['POST'])
def requestnewtimeslot():
	username=request.form['username']
	eid=request.form['eid']
	event=eventplanner(username)
	# pass real data here
	return render_template("eventplanner.html", name=username, events=event)

@app.route("/inventory", methods=['POST'])
def inventory():
	username=request.form['username']
	eid=request.form['selected_event']
	inventorylists=inventorylist(username,eid)
	stocks=totalitem()
	return render_template("inventory.html",name=username,eid=eid,inventory=inventorylists, stocks=stocks)

@app.route("/newitem",methods=['POST'])
def newitem():
	username=request.form['username']
	eid=request.form['eid']
	event=eventplanner(username)
	# pass real data here
	return render_template("eventplanner.html", name=username, events=event)





#venue
@app.route("/registervenue", methods=['POST'])
def registervenue():
	username=request.form["username"]
	vid=request.form["vid"]
	name=request.form["name"]
	address=request.form["address"]
	capacity=request.form["capacity"]
	facility=request.form["facility"]
	# pass real data here
	venue=venueowner(username)
	return render_template("venueowner.html", name=username, venue=venue)

@app.route("/managevenue", methods=['POST'])
def managevenue():
	username=request.form['username']
	# pass real data here
	venue=venueowner(username)
	return render_template("venueowner.html", name=username, venue=venue)


@app.route("/addtimeslot", methods=['POST'])
def addtimeslot():
	username=request.form['username']
	# pass real data here
	venue=venueowner(username)
	return render_template("venueowner.html", name=username, venue=venue)

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





#user
@app.route("/register", methods=['POST'])
def register():
	return render_template("register.html")

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
	#store in database
	return redirect(url_for("login"))	


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)