from django import forms

class CreateNewAccount(forms.Form):
    username = forms.CharField(label="Username",max_length=200)
    password = forms.CharField(label="Password", max_length=200)
    re_entered_pass = forms.CharField(label="Re-enter password", max_length=200)
