from django.urls import path
from .views import login, email_confirm

urlpatterns = [
    path('', login, name='sign-in'),
    path('email-confirm/<str:token>/', email_confirm, name='email-confirm')
]