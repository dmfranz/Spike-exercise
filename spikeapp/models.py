from django.db import models
from django.db.models.base import ModelState

# Create your models here.
class Login(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=500)
    