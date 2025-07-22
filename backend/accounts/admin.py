from django.contrib import admin
from .models import UserProfile, Tag

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Tag)