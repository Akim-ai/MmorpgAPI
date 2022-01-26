from django.urls import path
from src.oauth.endpoints.google.google import google_auth
from src.oauth.endpoints.login_register.login_or_register import login_or_register

urlpatterns = [
    path('google/', google_auth, name='google_auth'),
    path('', login_or_register, name='login_or_register'),
]
