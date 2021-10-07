from django import forms

class CreateNewRentalApplication(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=200)
    last_name = forms.CharField(label='Last Name', max_length=200)
    email = forms.CharField(label='Email', max_length=200)
    phone_number = forms.IntegerField(label='Phone number')

PRIORITY_CHOICES= [
    ('low', 'Low Priority'),
    ('high', 'Urgent'),
    ]

class CreateRequestForm(forms.Form):
    tenant_name= forms.CharField(label='Full Name', max_length=100)
    landlord_name= forms.CharField(label='Landlord Name', max_length=100)
    message= forms.CharField(label='Please enter your maintenance request here', widget=forms.Textarea(attrs={'style': "width:80%;"}), max_length=500)
    priority= forms.CharField(label='What is the priority?', widget=forms.Select(choices=PRIORITY_CHOICES))
