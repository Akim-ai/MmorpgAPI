from django.conf import settings
from django.shortcuts import render, redirect

from src.oauth.services.backend_auth import AuthBackend


def login(request):
    """
        Страница входа пользователя
    """
    return render(request, 'oauth/login.html')


def email_confirm(request, **kwargs):
    """
        Страница подтверждения емэйла
    """
    user = AuthBackend().authenticate_credential(token=kwargs.get('token', ''))[0]
    response: str
    token: str

    if not user.is_authenticated:
        user.is_authenticated = True
        user.save()
        response = 'Вы подтвердили ваш емаил, можете пользоваться сайтом'
        token = request.build_absolute_uri().split('/')[-2]
    else:
        return redirect('sign-in')
    return render(request, 'oauth/email-confirm.html', context={
        'response': response,
        'token': token,
    })
