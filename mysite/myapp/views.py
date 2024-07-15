from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.contrib.auth.models import User, auth
from django.contrib import messages
# from .models import Room
# Create your views here.


def index(request):
    return render(request, 'index.html')


def login(request):
    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username already taken')
                return redirect('register')
            elif User.objects.filer(username=username).isdigits().exist():
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, password=password)
                user.save();
                return redirect('login')
        else:
            messages.info(request, "password is not the same")
            return redirect('register')
    else:
        return render(request, 'signin.html')


def content(request):
    data = Feature.objects.all()
    context = {'data': data}
    return render(request, 'content.html', context)