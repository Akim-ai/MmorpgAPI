from django.shortcuts import render


def login(request):
    """
        Страница входа пользователя
    """
    return render(request, 'oauth/login.html')