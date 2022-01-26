from django.urls import path

from src.Profile.views import (profile_me, announcements_me)

urlpatterns = [
    path('', profile_me, name='profile-me'),
    path('announcement/', announcements_me, name='profile-me-announcements')
]