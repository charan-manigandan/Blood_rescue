from django.urls import path
from . import views
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name = "app"

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.login_user, name='login'),
    path('register', views.register, name='register'),
    path('donors', views.donors, name='donors'),
    path('logout', views.logout_user, name='logout'),
    path('edit_profile/<int:pk>', views.edit_profile, name='edit_profile'),
    path('view_profile/<int:pk>', views.view_profile.as_view(), name='view_profile'),
    path('create_profile', views.create_profile, name='create_profile'),
    path('send_otp', views.send_otp, name='send_otp'),
    path('verify_otp', views.verify_otp, name='verify_otp'),
    path('verified', views.verified, name='verified'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += staticfiles_urlpatterns()