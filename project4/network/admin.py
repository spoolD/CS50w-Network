from django.contrib import admin
from .models import User, Posting

# Register your models here.
admin.site.register(User)
admin.site.register(Posting)