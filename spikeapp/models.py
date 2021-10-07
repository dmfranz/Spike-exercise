from django.db import models
from django.db.models.base import ModelState


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

# PRIORITY_CHOICES = (
#     ('urgent','URGENT'),
#     ('low priority', 'LOW'),
# )

# class Priority(models.Model):
#     priority = models.CharField(max_length=2, choices=PRIORITY_CHOICES, default='low priority')

class RequestForm(models.Model):
    tenant_name = models.CharField(max_length=100)
    landlord_name = models.CharField(max_length=100)
    message = models.CharField(max_length=500)
    priority = models.CharField(max_length=100)