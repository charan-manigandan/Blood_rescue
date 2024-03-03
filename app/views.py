from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.response import Response
from .models import *
from django.contrib.auth import authenticate, login, logout
from datetime import datetime
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from .forms import Edit_profile, Create_Profile, VerifyForm
from django.views import View
from .serializers import *
from django.urls import reverse_lazy, reverse
from django.db.models import Q
import requests
import base64
import hmac
import hashlib
import pyotp
from .verify import send_otp
from datetime import datetime



# Create your views here.
def home(request):
        return render(request, 'home.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password =  request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            fname = user.first_name
            messages.success(request, "Logged In Sucessfully!!")
            return redirect('/')
        else:
            messages.error(request, "Wrong Credentials!!")
            return redirect('/login')
    
    return render(request, "login.html")

def register(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['first_name']
        lname = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('/register')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('/register')
        
        if len(username)>20:
            messages.error(request, "Username must be under 20 charcters!!")
            return redirect('/register')
        
        if password != confirm_password:
            messages.error(request, "Passwords didn't matched!!")
            return redirect('/register')
        
        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!!")
            return redirect('/register')
        
        myuser = User.objects.create_user(username, email, password)
        myuser.first_name = fname
        myuser.last_name = lname
        # myuser.is_active = False
        myuser.save()
        messages.success(request, "Your Account has been created succesfully!!")
        
        return redirect('/register')
        
    return render(request, "register.html")


def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged out ! ..."))
    return redirect('/')

@login_required(login_url='app:login')
def donors(request):
    blood_group = request.GET.get('blood_group')
    search_query = request.GET.get('search')
    donor_profiles = Donors.objects.all()

    if blood_group:
        donor_profiles = donor_profiles.filter(blood_group__iexact=blood_group)

    elif search_query:
        donor_profiles = donor_profiles.filter(
            Q(name__icontains=search_query) |
            Q(city__icontains=search_query) |
            Q(active_status__icontains=search_query)
        )
    context = {'donor_profiles': donor_profiles}
    return render(request, 'profile_list.html', context)

    
@login_required(login_url='app:login')
def create_profile(request):
    form = Create_Profile()
    if request.method == 'POST':
        form = Create_Profile(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
        messages.success(request, 'Your profile has been created successfully!')
        return redirect('app:donors')
    
    context = {'form': form}
    return render(request, 'profile.html', context)


def edit_profile(request, pk):
    donor = Donors.objects.get(id=request.user.donor.id)
    form = Edit_profile(instance=donor)

    if request.method == 'POST':
        form = Donors(request.POST,request.FILES,  instance=donor)
        if form.is_valid():
            form.save()
            return redirect('profile')

    context = {'form': form}
    return render(request, 'edit_profile.html', context)

class view_profile(View):
    def get(self, request, pk):
        add = Donors.objects.get(pk=request.user.donor.id)
        form = Create_Profile(instance=add)
        success_url = reverse_lazy('donors')
        return render(request,'view_profile.html', locals())

    def post(self, request, pk):
        donor = Donors.objects.get(id=request.user.donor.id)
        form = Edit_profile(request.POST, request.FILES, instance=donor)
        if form.is_valid():
            reg = Edit_profile(request.POST, request.FILES, instance=donor)
            reg.save()
        else:
            messages.warning(request, 'Invalid Input Data')
        return render(request, 'view_profile.html', locals())
    

# class donor(generics.ListCreateAPIView):
#     serializer_class = DonorSerializer
#     def get_queryset(self):
#         queryset = Donors.objects.all()
#         return queryset

# class donorDetail(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = DonorSerializer
#     queryset = Donors.objects.all()

def list_imgs(request):
    imgs = Donors.objects.all()
    context = {'imgs': imgs}
    return render(request, 'img.html', context)

def aadhaar_verification(request):
    if request.method == 'POST':
        aadhaar_number = request.POST.get('aadhaar_number')
        if aadhaar_number is None or not aadhaar_number.isdigit() or len(aadhaar_number) != 12:
            return render(request, 'verification.html', {'error': 'Invalid Aadhaar number'})
        url = "https://production.deepvue.tech/v1/otp"
        headers = {
            "accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "client_id": "YOUR_CLIENT_ID",
            "client_secret": "YOUR_API_KEY",
            "aadhaar_number": aadhaar_number
        }
        message = bytes(str(data), "utf-8")
        secret = bytes("YOUR_API_SECRET", "utf-8")
        hash = hmac.new(secret, message, hashlib.sha256)
        signature = base64.b64encode(hash.digest()).decode()
        headers["Authorization"] = f"HMAC-SHA256 {signature}"
        response = requests.post(url, headers=headers, data=data)

        if response.status_code == 200:
            response_json = response.json()
            otp = response_json["data"]["otp"]
            return render(request, 'otp.html', {'aadhaar_number': aadhaar_number, 'otp': otp})
        else:
            return render(request, 'verification.html', {'error': 'Request failed'})
    else:
        return render(request, 'verification.html')
