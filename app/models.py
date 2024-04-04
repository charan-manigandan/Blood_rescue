from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from indian_cities.dj_city import cities
from django.core.exceptions import PermissionDenied

# Create your models here.
blood_types = (("O +ve", "O +ve"), ("O -ve", "O -ve"), ("A +ve", "A +ve"), ("A -ve", "A -ve"), 
               ("B +ve", "B -ve"), ("B -ve", "B -ve"), ("AB +ve", "AB +ve"), ("AB -ve", "AB -ve"), 
               ("A1 +ve", "A1 +ve"), ("A1 -ve", "A1 -ve"), ("A1B +ve", "A1 +ve"), ("A1B -ve", "A1 -ve"), 
               ("A2 +ve", "A2 +ve"), ("A2 -ve", "A2 -ve"), ("A2B +ve", "A2B +ve"), ("A2B -ve", "A2B -ve"), 
               ("INRA", "INRA"), ("Bombay Blood Group", "Bombay Blood Group"))
active_status = (('Active', 'Active'),('Not Active', 'Not Active'))

class Donors(models.Model):
    user = models.OneToOneField(User, related_name='donor', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=False)
    age = models.BigIntegerField(null=False)
    ph_num = models.CharField(max_length=10, null=True)
    date_created = models.DateField(auto_now_add=True)
    blood_group = models.CharField(choices=blood_types, max_length=20, null=False)
    date_modified = models.DateField(auto_now=True)
    city = models.CharField(choices=cities, max_length=20)
    address = models.CharField(max_length=100, null=True)
    active_status = models.ImageField(default='Active',max_length=10, choices=active_status)

    def __str__(self):
        return self.name

    @property
    def blood_types(self):
        return (
            ("O +ve", "O +ve"), ("O -ve", "O -ve"), ("A +ve", "A +ve"), ("A -ve", "A -ve"),
            ("B +ve", "B -ve"), ("B -ve", "B -ve"), ("AB +ve", "AB +ve"), ("AB -ve", "AB -ve"),
            ("A1 +ve", "A1 +ve"), ("A1 -ve", "A1 -ve"), ("A1B +ve", "A1 +ve"), ("A1B -ve", "A1 -ve"),
            ("A2 +ve", "A2 +ve"), ("A2 -ve", "A2 -ve"), ("A2B +ve", "A2B +ve"), ("A2B -ve", "A2B -ve"),
            ("INRA", "INRA"), ("Bombay Blood Group", "Bombay Blood Group")
        )

class Verification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    verified = models.BooleanField(default=False)

class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    report = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)