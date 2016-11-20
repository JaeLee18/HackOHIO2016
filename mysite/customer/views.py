from django.shortcuts import render
from django.http import HttpResponse
from .forms import *
import pyrebase

# Create your views here.
def index(request):
	return render(request, 'index.html')

def check(request):
	return render ("index.html")

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

	

	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			email = form['username'].value()
			print (email)
			password = form['password'].value()
			print (password)
			# Log the user in
			user = auth.create_user_with_email_and_password(email, password)
			return render(request, 'register_done.html')
	else:
		form = LoginForm()
	return render(request, 'register.html', {'form': form})
