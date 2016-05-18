from django import forms
from kaizing.models import *

class VendorLoginForm(forms.ModelForm):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)
	class Meta:
		model = Vendor
		fields = ('username', 'password')