from django import forms

class LoginForm(forms.Form):
	username = forms.CharField(widget = forms.EmailInput)
	password = forms.CharField(widget = forms.PasswordInput)
	name = forms.CharField()


class UserInfo(forms.Form):
	username = forms.CharField(widget = forms.EmailInput)
	password = forms.CharField(widget = forms.PasswordInput)

class PasswordReset(forms.Form):
	username = forms.CharField(widget = forms.EmailInput)

class GroupForm(forms.Form):
	groupTitle = forms.CharField()