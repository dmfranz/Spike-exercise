from django.db import models
from django.db.models.base import ModelState
from django.core.validators import MinValueValidator


# Create your models here.
class Login(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=500)


class RentalApplication(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone_number = models.IntegerField(default=None)


class User(models.Model):
    username = models.CharField(max_length=200)
    is_renter = models.BooleanField(default=False)


class Payment(models.Model):
    # Support is being left in for multiple payment methods, but currently hard-coded to debit.
    ETRANSFER = 'ETR'
    ECHECK = 'ECH'
    DEBIT = 'DBT'
    PAYMENT_CHOICES = [
        (ETRANSFER, 'Electronic Transfer'),
        (ECHECK, 'eCheck'),
        (DEBIT, 'Debit Card')
    ]

    ByTenant = models.BooleanField(default=True)
    # Because this can be done by an owner on behalf of a tenant, we need to record
    # who is making the deposit and whose account it will affect.
    DepositingUser = models.CharField(max_length=100)
    AffectedUser = models.CharField(max_length=100)
    Amount = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.01)])
    RunningBalance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    Method = models.CharField(max_length=3, choices=PAYMENT_CHOICES, default='DBT')
