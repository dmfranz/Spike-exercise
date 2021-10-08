from django import forms
from django.forms import ModelForm
from spikeapp.models import Payment
from spikeapp.cardhandling import CreditCardField
from spikeapp.cardhandling import CreditCardExpirationField


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

class MakePayment(ModelForm):
    class Meta:
        model = Payment
        exclude = ['ByRenter', 'RunningBalance', 'Method']
        labels = {
            "Amount": "Payment Amount"
        }
        placeholders = {
            "Amount": 0.00
        }

    CardNum = CreditCardField(label='Card Number',
                              placeholder=u'0000 0000 0000 0000',
                              min_length=12,
                              max_length=19)
    CardDate = CreditCardExpirationField(label='Card Expiration Date')
    CardCVV = forms.IntegerField(label='Card CVV',
                                 max_value=9999,
                                 min_value=0)
    CardName = forms.CharField(label='Name on Card',
                               min_length=2,
                               max_length=26)
