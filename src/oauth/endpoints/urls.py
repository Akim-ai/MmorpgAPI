from django.urls import path
from src.oauth.endpoints.google.google import google_auth


urlpatterns = [
    path('google/', google_auth, name='google_auth')
]
