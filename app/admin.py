from django.contrib import admin
from .models import *
from django.contrib.auth.models import Group, User

# Register your models here.
admin.site.unregister(Group)

class ProfileInline(admin.StackedInline):
    model = Donors

class UserAdmin(admin.ModelAdmin):
    model = User
    fields = '__all__'
    inlines = [ProfileInline]

admin.site.register(Donors)
admin.site.register(Verification)