from django.shortcuts import render
from django.http import HttpResponse
from .forms import *
import pyrebase
from django.contrib.sessions.models import Session
from django.core.mail import EmailMessage

import requests
import json
# Create your views here.
def index(request):
	return render(request, 'index.html')

def check(request):
	return render (request, "login_done.html")
def confirm(request):
	config = {
  	"apiKey": "AIzaSyDJBkHwuCdQuaeeS2GsZ8bYHoV8L2jbb2Q",
  	"authDomain": "travelone-e43cb.firebaseapp.com",
  	"databaseURL": "https://travelone-e43cb.firebaseio.com/",
  	"storageBucket": "travelone-e43cb.appspot.com"
	}
	firebase = pyrebase.initialize_app(config)
	if request.method == 'POST':
		form = ConfirmForm(request.POST)
		if form.is_valid():
			location = form['location'].value()
			hotel = form['hotel'].value()
			price = form['price'].value()
			gid = request.session['GID']
			data={"hotel": hotel, "location": location, "price":price}
			db = firebase.database()
			db.child('group').child(gid).child("request").update(data)
			size = len(request.session['invitee'])
			price = int(price)/int(size)
			return render(request, "confirmed_group.html", {"size":size,"title":request.session['TITLE'], "owner":request.session['OWNER'], "gid":request.session['GID'],"hotel":hotel, "location":location,"names":request.session['invitee'],"price":price})
	else:
		form = ConfirmForm()
	return render(request, "manage_group.html", {"form": form} )

def transfer(request):
	if request.method == 'POST':
		form = TransferForm(request.POST)
		if form.is_valid():
			amount = form['amount'].value()
			payee_id = form['payee_id'].value()
			description = form['description'].value()
			accountID = request.session['THISID']
			apiKey = '4bc490818e16f32a0267a6170e4e1a4b'
			url = 'http://api.reimaginebanking.com/accounts/{}/transfers?key={}'.format(accountID,apiKey)
			payload = {
			  "medium": "balance",
			  "payee_id": payee_id,
			  "amount": amount,
			  "transaction_date": "2016-11-20",
			  "description": description
			}
			response = requests.post( 
			url, 
			data=json.dumps(payload),
			headers={'content-type':'application/json'},
			)
			url = "http://api.reimaginebanking.com/accounts/{}?key=4bc490818e16f32a0267a6170e4e1a4b".format(accountID)
			r = requests.get(url)
			print(r.json())
			a = r.json()
			print(a)
			print(a['balance'])	
		
			if response.status_code != 404:
				return render(request, 'transfer_success.html', {'payee_id':payee_id, 'amount':amount, "balance": a['balance'], "nickname":a['nickname']})
			else:
				return HttpResponse("Invalid inputs")
			print("response: " , response.status_code)
	else:
		form = TransferForm()
	return render(request, 'transfer.html', {"form":form})

def ConnectBank(request):
	config = {
  	"apiKey": "AIzaSyDJBkHwuCdQuaeeS2GsZ8bYHoV8L2jbb2Q",
  	"authDomain": "travelone-e43cb.firebaseapp.com",
  	"databaseURL": "https://travelone-e43cb.firebaseio.com/",
  	"storageBucket": "travelone-e43cb.appspot.com"
	}
	firebase = pyrebase.initialize_app(config)
	auth = firebase.auth()

	uid = request.session['uid']
	db = firebase.database()
	if request.method == 'POST':
		form = CustomerId(request.POST)
		if form.is_valid():
			cid = form['customerID'].value()
			url = "http://api.reimaginebanking.com/customers/{}/accounts?key=4bc490818e16f32a0267a6170e4e1a4b".format(cid)
			r = requests.get(url)
			if r.status_code == 200:
				myuser = db.child("users").get()
				a = list(r.json())
				myDict = a[0]
				myId = myDict['_id']
				request.session['THISID'] = myId
				for u in myuser.each():
					if u.key() == request.session['uid']:
						data = {'customerID':myId}
						db.child('users').child(request.session['uid']).update(data)
				return render(request, 'connectBank_done.html', {"myDict":myDict})
			else:
				return HttpResponse("Invalid Customer ID")
	else:
		form = CustomerId()
	return render(request, 'connectBank.html', {"form":form})




	return render(request, "connectBank_done.html")
def JoinGroup(request):
	config = {
  	"apiKey": "AIzaSyDJBkHwuCdQuaeeS2GsZ8bYHoV8L2jbb2Q",
  	"authDomain": "travelone-e43cb.firebaseapp.com",
  	"databaseURL": "https://travelone-e43cb.firebaseio.com/",
  	"storageBucket": "travelone-e43cb.appspot.com"
	}
	firebase = pyrebase.initialize_app(config)

	# Get a reference to the auth service
	auth = firebase.auth()

	uid = request.session['uid']
	db = firebase.database()
	groups = db.child("group").get()
	groupID = ""
	myTitle = ""
	owner = ""
	if request.method == 'POST':
		form = GetGroup(request.POST)
		if form.is_valid():
			code = form['groupID'].value()
			request.session['GID'] = code
			searched = False
			for g in groups.each():
				if g.key() == code:
					searched = True
					myTitle = g.val()['title']
					owner = g.val()['name']
					request.session['OWNER'] = owner
					request.session['TITLE'] = myTitle
					groupId = g.key()
				
					data = {"inviteeName": request.session['myName']}
					db.child("group").child(groupId).child("invitee").push(data)
					print("myname: " ,request.session['myName'])
					return render(request, 'invitation_success.html', {"title":myTitle, "owner":owner, "gid":groupId})
			if searched == False:
				return HttpResponse("Invalid Group code")
	else:
		form = GetGroup()
	return render(request, 'joinGroup.html', {'form': form}) 

def GroupView(request):
	config = {
  	"apiKey": "AIzaSyDJBkHwuCdQuaeeS2GsZ8bYHoV8L2jbb2Q",
  	"authDomain": "travelone-e43cb.firebaseapp.com",
  	"databaseURL": "https://travelone-e43cb.firebaseio.com/",
  	"storageBucket": "travelone-e43cb.appspot.com"
	}
	firebase = pyrebase.initialize_app(config)

	# Get a reference to the auth service
	auth = firebase.auth()

	uid = request.session['uid']
	db = firebase.database()
	groups = db.child("group").get()
	#print (groups.val())
	groupID = ""
	myTitle = ""
	owner = ""
	for u in groups.val():
		for g in groups.each():
			for key, value in g.val().items():
				if uid == value:
					groupID = u
					myTitle = g.val()['title']
					owner = g.val()['name']
	print(groupID)

	names = []
	
	for g in groups.each():
		if g.key() == request.session['GID']:
			obj = g.val()
			objj = obj.get('invitee')
			key = objj.keys()
			key = list(objj)
			for i in range(0, len(key)):
				names.append(objj[key[i]]['inviteeName'])
	hotel = []
	groups = db.child("hotel").get()
	for g in groups.each():
		hotel.append(g.val())
	location = []
	groups = db.child("location").get()
	for g in groups.each():
		location.append(g.val())


	print(names)
	print(request.session['GID'])

	request.session['invitee'] = names
	form = ConfirmForm()
	return render(request,'manage_group.html', {'gid':request.session['GID'], 'title':request.session['TITLE'], 'owner':request.session['OWNER'], 'names':names, 'location':location, 'hotel':hotel, 'form':form})
            


def pw_reset(request):
	config = {
  	"apiKey": "AIzaSyDJBkHwuCdQuaeeS2GsZ8bYHoV8L2jbb2Q",
  	"authDomain": "travelone-e43cb.firebaseapp.com",
  	"databaseURL": "https://travelone-e43cb.firebaseio.com/",
  	"storageBucket": "travelone-e43cb.appspot.com"
	}
	firebase = pyrebase.initialize_app(config)

	# Get a reference to the auth service
	auth = firebase.auth()
	if request.method == 'POST':
		form = PasswordReset(request.POST)
		if form.is_valid():
			email = form['username'].value()
			print (email)
			auth.send_password_reset_email(email)
			return render(request, 'pw_reset_done.html', {'email':email})
	else:
		form = PasswordReset()
	return render(request, 'pw_reset.html', {'form': form}) 

def login(request):
	config = {
  	"apiKey": "AIzaSyDJBkHwuCdQuaeeS2GsZ8bYHoV8L2jbb2Q",
  	"authDomain": "travelone-e43cb.firebaseapp.com",
  	"databaseURL": "https://travelone-e43cb.firebaseio.com/",
  	"storageBucket": "travelone-e43cb.appspot.com"
	}
	firebase = pyrebase.initialize_app(config)

	# Get a reference to the auth service
	auth = firebase.auth()
	db = firebase.database()
	if request.method == 'POST':
		form = UserInfo(request.POST)
		if form.is_valid():
			email = form['username'].value()
			
			password = form['password'].value()
			
			user = auth.sign_in_with_email_and_password(email, password)
			# Get all users
			myuser = db.child("users").get()
			# Get an email from logged in user
			email = user.get('email')
			uid = ""
			myName = ""
			for u in myuser.each():
				for key,value in u.val().items():
					if email == value:
						uid = u.key()
			for u in myuser.each():
				if u.key() == uid:
					for key,value in u.val().items():
						if key == "name":
							myName = value

			request.session['uid'] = uid
			request.session['myName'] = myName



			return render(request, 'login_done.html', {'myName': request.session['myName']})
	else:
		form = UserInfo()
	return render(request, 'login.html', {'form': form})
def makeGroup(request):
	uid = request.session['uid']
	config = {
  	"apiKey": "AIzaSyDJBkHwuCdQuaeeS2GsZ8bYHoV8L2jbb2Q",
  	"authDomain": "travelone-e43cb.firebaseapp.com",
  	"databaseURL": "https://travelone-e43cb.firebaseio.com/",
  	"storageBucket": "travelone-e43cb.appspot.com"
	}
	firebase = pyrebase.initialize_app(config)

	# Get a reference to the auth service
	auth = firebase.auth()
	db = firebase.database()
	myName = request.session['myName']
	print("UID: ", uid)
	if request.method == 'POST':
		form = GroupForm(request.POST)
		if form.is_valid():
			title = form['groupTitle'].value()
			data = {"groupOwnerUID" : uid, "title": title, "name": myName}
			db.child("group").push(data)	
			return render(request, 'group_done.html', {'title': title, 'myName' : myName})
	else:
		form = GroupForm()
	return render(request, 'group.html', {'form': form, 'myName': myName})
def register(request):
	config = {
  	"apiKey": "AIzaSyDJBkHwuCdQuaeeS2GsZ8bYHoV8L2jbb2Q",
  	"authDomain": "travelone-e43cb.firebaseapp.com",
  	"databaseURL": "https://travelone-e43cb.firebaseio.com/",
  	"storageBucket": "travelone-e43cb.appspot.com"
	}
	firebase = pyrebase.initialize_app(config)

	# Get a reference to the auth service
	auth = firebase.auth()

	# Get a db 
	db = firebase.database()

	
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			email = form['username'].value()
			#print (email)
			password = form['password'].value()
			#print (password)
			# Log the user in
			name = form['fullname'].value()
			user = auth.create_user_with_email_and_password(email, password)
			data = {"username": email, "name": name}
			db.child("users").push(data)
			return render(request, 'register_done.html', {'name': name})
	else:
		form = LoginForm()
	return render(request, 'register.html', {'form': form})
