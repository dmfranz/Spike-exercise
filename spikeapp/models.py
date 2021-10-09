from django.db import models
from django.db.models.base import ModelState
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=200, blank=True)
    is_renter = models.BooleanField(default=False)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(username=instance)
    instance.profile.save()


class RentalApplication(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone_number = models.IntegerField(default=None)


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

    ByRenter = models.BooleanField(default=True)
    Amount = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.01)])
    RunningBalance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    Method = models.CharField(max_length=3, choices=PAYMENT_CHOICES, default='DBT')
