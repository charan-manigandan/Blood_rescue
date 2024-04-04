from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.forms.widgets import FileInput
from .models import Donors, Report

class Create_Profile(ModelForm):

    class Meta:
        model = Donors
        exclude = ['user']
        fields = '__all__'

class Edit_profile(forms.ModelForm):
        
    class Meta:
        model = Donors
        fields = "__all__"
        exclude = ['user']

class VerifyForm(forms.Form):
    adhaar_number = forms.CharField(max_length=12)
    phone_number = forms.CharField(max_length=10)
    otp = forms.CharField(max_length=6)

class ReportForm(forms.Form):
    report = forms.CharField(max_length=1000)

    class Meta:
        model = Report
        fields = "__all__"
        exclude = ['user']