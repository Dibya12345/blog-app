from django.contrib import admin

# Register your models here.
from .models import Blog, User

admin.site.register(Blog)
admin.site.register(User)