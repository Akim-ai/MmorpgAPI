from django.http import JsonResponse
from rest_framework.parsers import JSONParser, MultiPartParser

from src.oauth.models import Auth as User, Avatar
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import get_object_or_404
from rest_framework.views import Response, APIView
from .serializers import (ProfileSelfSerializer,
                          ProfileSerializer,
                          UserAvatar)
from ...Announcements.endpoints.custom_renders import JPEGRenderer, PNGRenderer


class UserSelfProfileView(RetrieveAPIView):
    """
    User Self Profile View
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSelfSerializer

    def get_queryset(self):
        return self.request.user

    def get_object(self):
        return self.get_queryset()


class UserProfileView(RetrieveAPIView):
    """
    Profile View
    """
    permission_classes = [IsAuthenticated, ]
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return User.objects.get(id=self.kwargs['pk'])

    def get_object(self):
        return self.get_queryset()


class ProfileAvatar(APIView):
    """
    Profile Avatar
    """
    renderer_classes = [PNGRenderer, JPEGRenderer]

    def get(self, request, *args, **kwargs):
        img = get_object_or_404(Avatar, img=self.kwargs['img'], deleted=False)
        return Response(img.img)

    def put(self, request, *args, **kwargs):
        serializer = UserAvatar
        return Response(status=200)
