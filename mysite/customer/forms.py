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
	groupTitle = forms.CharField(label = "Group Title")

class InviteFriends(forms.Form):
	Invite = forms.CharField(widget = forms.EmailInput)

class GetGroup(forms.Form):
	groupID = forms.CharField(label = "Group ID")

class CustomerId(forms.Form):
	customerID = forms.CharField(label = "Customer ID")

class TransferForm(forms.Form):
	amount = forms.CharField()
	payee_id = forms.CharField()
	description = forms.CharField()

class ConfirmForm(forms.Form):
	HOTEL = (("Morning Inn", "Morning Inn"), ('Ohio Inn', 'Ohio Inn'), ('Purdue Inn', 'Purdue Inn'))
	LOCATION = (('Chicago', "Chicago"), ('Los Angeles', 'Los Angeles'), ('Las Vegas', 'Las Vegas'), ('New York', 'New York'), ('Washington DC', 'Washington DC'))
	hotel = forms.ChoiceField(choices = HOTEL)
	location = forms.ChoiceField(choices = LOCATION)
	price = forms.CharField()