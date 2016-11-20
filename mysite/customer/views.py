from django.shortcuts import render
from django.http import HttpResponse
from .forms import *
import pyrebase
from django.contrib.sessions.models import Session
# Create your views here.
def index(request):
	return render(request, 'index.html')

def check(request):
	return render ("index.html")
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

			return render(request, 'login_done.html', {'myName': myName})
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
			data = {"groupOwnerUID" : uid, "title": title}
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
			name = form['name'].value()
			user = auth.create_user_with_email_and_password(email, password)
			data = {"username": email, "name": name}
			db.child("users").push(data)
			return render(request, 'register_done.html', {'name': name})
	else:
		form = LoginForm()
	return render(request, 'register.html', {'form': form})
