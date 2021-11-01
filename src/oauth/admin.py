from django.contrib import admin
from .models import Auth, Avatar, Follower

# Register your models here.
admin.site.register(Auth)
admin.site.register(Avatar)
admin.site.register(Follower)

