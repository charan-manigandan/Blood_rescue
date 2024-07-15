from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('login/signin/', views.register, name='signin'),
    path('content/', views.content, name='content')
]