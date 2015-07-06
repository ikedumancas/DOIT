from django.contrib import admin
from django.contrib.auth.models import Group
from .models import UserProfile
# Register your models here.
admin.site.register(UserProfile)
admin.site.unregister(Group)