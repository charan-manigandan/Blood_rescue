from django.db import models, migrations
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

# # Create your models here.

# def Room(models.Model):
#     name = models.CharField(max_length=200)
#     return name
#
#     def __str__(self):
#         return self.name


class Feature(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    age = models.IntegerField(default=00, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=False)
    phone = PhoneNumberField(null=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.name
