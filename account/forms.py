from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class UserRegistrationForm (UserCreationForm):
    referral = forms.CharField(label='Referral Username', max_length= 64, required = False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Referral Username'}))
    first_name = forms.CharField(label='First Name', max_length= 64, required = True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'First Name'}))
    last_name = forms.CharField(label='Last Name', max_length= 64, required = True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Last Name'}))
    tpin1 = forms.CharField(label='Transaction Pin', max_length= 4, required = True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Transaction Pin'}))
    tpin2 = forms.CharField(label='Confirm Transaction Pin', max_length= 4, required = True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Confirm Transaction Pin'}))
    terms= forms.BooleanField(required= True)
    password1 = forms.CharField(max_length=16, required = True, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(max_length=16, required = True, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))
    country = forms.CharField(label='Country', max_length= 120, required = True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Country'}))

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "first_name", "last_name", "referral", "tpin1", "tpin2", "country"]
        widgets = {
        'email' : forms.EmailInput(attrs={'class': 'form-control required', 'placeholder':'Email@address.com'}),
        'username' : forms.TextInput(attrs={'class': 'form-control required', 'placeholder':'Username'})
        }

class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model= Profile
        fields = ["address", "phone_number", "city", "state", "country"]
        widgets = {
        "address": forms.TextInput(attrs={'class': 'form-control'}),
        "phone_number":forms.TextInput(attrs={'class': 'form-control'}),
        "city": forms.TextInput(attrs={'class': 'form-control'}),
        "state": forms.TextInput(attrs={'class': 'form-control'}),
        "country": forms.TextInput(attrs={'class': 'form-control'})
        }
        labels = {
        "address": "Address",
        "phone_number":"Phone Number",
        "city": "City",
        "state": "State",
        "country": "Country"
        }
