# A card-handling algorithm from Chris Kief
# https://chriskief.com/2017/06/17/django-form-credit-card-field-with-pattern-length-and-luhn-validation/

from django import forms
from django.forms.widgets import TextInput
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinValueValidator
import datetime
import calendar


class TelephoneInput(TextInput):
    # switch input type to type tel so that the numeric keyboard shows on mobile devices
    input_type = 'tel'


class CreditCardField(forms.CharField):
    # validates almost all of the example cards from PayPal
    # https://www.paypalobjects.com/en_US/vhelp/paypalmanager_help/credit_card_numbers.htm
    cards = [
        {
            'type': 'maestro',
            'patterns': [5018, 502, 503, 506, 56, 58, 639, 6220, 67],
            'length': [12, 13, 14, 15, 16, 17, 18, 19],
            'cvvLength': [3],
            'luhn': True
        }, {
            'type': 'forbrugsforeningen',
            'patterns': [600],
            'length': [16],
            'cvvLength': [3],
            'luhn': True
        }, {
            'type': 'dankort',
            'patterns': [5019],
            'length': [16],
            'cvvLength': [3],
            'luhn': True
        }, {
            'type': 'visa',
            'patterns': [4],
            'length': [13, 16],
            'cvvLength': [3],
            'luhn': True
        }, {
            'type': 'mastercard',
            'patterns': [51, 52, 53, 54, 55, 22, 23, 24, 25, 26, 27],
            'length': [16],
            'cvvLength': [3],
            'luhn': True
        }, {
            'type': 'amex',
            'patterns': [34, 37],
            'length': [15],
            'cvvLength': [3, 4],
            'luhn': True
        }, {
            'type': 'dinersclub',
            'patterns': [30, 36, 38, 39],
            'length': [14],
            'cvvLength': [3],
            'luhn': True
        }, {
            'type': 'discover',
            'patterns': [60, 64, 65, 622],
            'length': [16],
            'cvvLength': [3],
            'luhn': True
        }, {
            'type': 'unionpay',
            'patterns': [62, 88],
            'length': [16, 17, 18, 19],
            'cvvLength': [3],
            'luhn': False
        }, {
            'type': 'jcb',
            'patterns': [35],
            'length': [16],
            'cvvLength': [3],
            'luhn': True
        }
    ]

    def __init__(self, placeholder=None, *args, **kwargs):
        super(CreditCardField, self).__init__(
            # override default widget
            widget=TelephoneInput(attrs={
                'placeholder': placeholder
            }),
            *args, **kwargs)

    default_error_messages = {
        'invalid': _(u'The credit card number is invalid'),
    }

    def clean(self, value):

        # ensure no spaces or dashes
        value = value.replace(' ', '').replace('-', '')

        # get the card type and its specs
        card = self.card_from_number(value)

        # if no card found, invalid
        # if not card:
        #     raise forms.ValidationError(self.error_messages['invalid'])
        #
        # # check the length
        # if not len(value) in card['length']:
        #     raise forms.ValidationError(self.error_messages['invalid'])
        #
        # # test luhn if necessary
        # if card['luhn']:
        #     if not self.validate_mod10(value):
        #         raise forms.ValidationError(self.error_messages['invalid'])

        return value

    def card_from_number(self, num):
        # find this card, based on the card number, in the defined set of cards
        for card in self.cards:
            for pattern in card['patterns']:
                if str(pattern) == str(num)[:len(str(pattern))]:
                    return card

    def validate_mod10(self, num):
        # validate card number using the Luhn (mod 10) algorithm
        checksum, factor = 0, 1
        for c in reversed(num):
            for c in str(factor * int(c)):
                checksum += int(c)
            factor = 3 - factor
        return checksum % 10 == 0


# Expiration date handling by Julian Wachholz:
# https://gist.github.com/julianwachholz/6719216
class CreditCardExpirationField(forms.DateField):
    default_error_messages = {
        'min_value': _("This card has expired."),
        'invalid': _("Please specify a valid expiration date.")
    }
    widget = forms.DateInput(format='%m/%Y')
    input_formats = ('%m/%Y', '%m/%y')
    default_validators = [
        MinValueValidator(datetime.datetime.now().date()),
    ]

    def to_python(self, value):
        """
        Set day to last day of month.
        Credit cards are valid through the last day of the specified month.
        """
        value = super(CreditCardExpirationField, self).to_python(value)
        last_day = calendar.monthrange(value.year, value.month)[1]
        return datetime.date(value.year, value.month, last_day)


def TryPayment(MakePayment):
    # A function to serve as a fake handler of card payments
    # For ease of testing, this will only fail if the input CVV is 420
    CVV = MakePayment.cleaned_data.get("CardCVV")
    if CVV == 420:
        return False
    else:
        return True
