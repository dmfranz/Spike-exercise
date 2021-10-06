from django import forms

class CreateNewRentalApplication(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=200)
    last_name = forms.CharField(label='Last Name', max_length=200)
    email = forms.CharField(label='Email', max_length=200)
    phone_number = forms.IntegerField(label='Phone number')
