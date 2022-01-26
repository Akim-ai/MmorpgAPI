from django.shortcuts import render

# Create your views here.
from config import settings


def profile_me(request):
    return render(request, template_name='Profile/profile-me.html', context={
        'api': f'{settings.API_AND_VERSION}'
    })


def announcements_me(request):
    return render(request, template_name='Profile/Announcements/announcements-me.html', context={
        'api': f'{settings.API_AND_VERSION}'
    })