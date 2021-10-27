from rest_framework.decorators import api_view
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response

from config import settings
from src.oauth.endpoints.serializers import GoogleAuth
from google.oauth2 import id_token
from google.auth.transport import requests

from src.oauth.models import Auth

from src.oauth.services.auth_base import create_token


@api_view(["POST"])
def google_auth(request):
    """
    Подтверждение авторизации через гугл
    """
    google_data = GoogleAuth(data=request.data)
    if google_data.is_valid():
        token = check_google_auth(google_data.data)
        return Response(token)
    else:
        return AuthenticationFailed(code=403, detail='Bad data google')


def check_google_auth(google_user: GoogleAuth) -> dict:
    try:
        id_token.verify_oauth2_token(google_user['token'], requests.Request(), settings.GOOGLE_CLIENT_ID)
    except ValueError:
        raise AuthenticationFailed(code=403, detail='Bad token Google')

    user, _ = Auth.objects.get_or_create(email=google_user['email'])
    return create_token(user.id)
