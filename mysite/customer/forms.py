from django import forms

class LoginForm(forms.Form):
	username = forms.CharField(widget = forms.EmailInput)
	password = forms.CharField(widget = forms.PasswordInput)
	fullname = forms.CharField()


class UserInfo(forms.Form):
	username = forms.CharField(widget = forms.EmailInput,error_messages={'required':'Enter a valid username'})
	password = forms.CharField(widget = forms.PasswordInput,error_messages={'required':'Enter a valid password'})

class PasswordReset(forms.Form):
	username = forms.CharField(widget = forms.EmailInput)

class GroupForm(forms.Form):
	groupTitle = forms.CharField()

class InviteFriends(forms.Form):
	Invite = forms.CharField(widget = forms.EmailInput)

class GetGroup(forms.Form):
	groupID = forms.CharField()