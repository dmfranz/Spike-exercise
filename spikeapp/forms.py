from django import forms
from spikeapp.models import Payment, RequestForm, RentalApplication
from django.forms import ModelForm, Textarea
from spikeapp.models import Payment, RequestForm, OwnerFee
from spikeapp.cardhandling import CreditCardField
from spikeapp.cardhandling import CreditCardExpirationField
from spikeapp.models import Profile


class ProfileForm(ModelForm):
    fullname = forms.CharField(label="Full Name", max_length=200)
    is_renter = forms.CheckboxInput()

    class Meta:
        model = Profile
        fields = ("fullname", "is_renter", )


class CreateNewRentalApplication(ModelForm):
    landlord = forms.CharField(label='Landlord', max_length=200)
    first_name = forms.CharField(label='First Name', max_length=200)
    last_name = forms.CharField(label='Last Name', max_length=200)
    email = forms.CharField(label='Email', max_length=200)
    phone_number = forms.CharField(label='Phone number', max_length=200)

    class Meta:
        model = RentalApplication
        fields = ("landlord", "first_name", "last_name", "email", "phone_number")


PRIORITY_CHOICES = [
    ('low', 'Low Priority'),
    ('high', 'Urgent'),
]


class CreateRequestForm(forms.ModelForm):
    tenant_name = forms.CharField(label='Full Name', max_length=100)
    landlord_name = forms.CharField(label='Landlord Name', max_length=100)
    message = forms.CharField(label='Please enter your maintenance request here', widget=forms.Textarea(attrs={'style': "width:80%;"}), max_length=500)
    priority = forms.CharField(label='What is the priority?', widget=forms.Select(choices=PRIORITY_CHOICES))

    class Meta:
        model = RequestForm
        exclude = ('response',)


class ManageRequestForm(forms.ModelForm):
    response = forms.CharField(label='Owner Comments', widget=forms.Textarea(attrs={'style': "width:80%;"}), max_length=500)

    class Meta:
        model = RequestForm
        exclude = ['tenant_name', 'landlord_name', 'message', 'priority']


class MakePayment(ModelForm):
    class Meta:
        model = Payment
        exclude = ['Method']
        labels = {
            "Amount": "Payment Amount",
            "AffectedUser": "Account for Deposit (username)"
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


class OwnerFeeForm(ModelForm):
    class Meta:
        model = OwnerFee
        fields = '__all__'
        labels = {
            "Amount": "Fee Amount",
            "Note": "Fee Notes",
            "AffectedUser": "Account for Deposit (username)"
        }
        widgets = {
            'Note': Textarea(attrs={'style': "width:80%;"}),
        }
        placeholders = {
            "Amount": 0.00
        }
