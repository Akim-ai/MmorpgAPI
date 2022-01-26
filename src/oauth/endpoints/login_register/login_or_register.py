from django.conf import settings

from ..serializers import LoginOrRegister
from rest_framework.decorators import api_view

from src.oauth.models import Auth as User
from ...services.auth_base import create_token

from rest_framework.response import Response

from src.oauth.tasks import send_confirm_email


@api_view(["POST"])
def login_or_register(request):
    serializer = LoginOrRegister(data=request.data)
    print(request.data)
    if serializer.is_valid():

        data = serializer.data
        user: User = User()
        try:
            user = User.objects.get(email=data.get('email'), password=data.get('password'))
        except Exception as e:
            user = User.objects.create(email=data.get('email'), password=data.get('password'))
        finally:

            if not user.is_authenticated:
                token = create_token(user.id)
                send_confirm_email.delay(user_email=str(user.email), token=token.get('access_token'))
                return Response(
                    {'data': 'В течении минут к нам на почту придет письмо с ссылкой для активации аккаунта. ',
                     'token': 0, 'user_id': 0},
                    status=201
                )
            return Response(
                {'data': 'Вы авторизованный пользователь', **create_token(user.id)}, status=200
            )
    return Response(status=404)
