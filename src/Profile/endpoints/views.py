from django.http import JsonResponse
from django.shortcuts import redirect
from rest_framework.parsers import JSONParser, MultiPartParser

from config import settings
from src.oauth.models import Auth as User, Avatar
from rest_framework.generics import RetrieveAPIView, UpdateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import get_object_or_404
from rest_framework.views import Response, APIView

from utils.permissions import IsOwner
from .serializers import (
    ProfileSelfSerializer,
    ProfileSerializer,
    UserAvatar)
from ...Announcements.endpoints.custom_renders import JPEGRenderer, PNGRenderer


class UserSelfProfileView(RetrieveAPIView, UpdateAPIView):
    """
    User Self Profile View
    """
    permission_classes = [IsOwner]
    serializer_class = ProfileSelfSerializer
    http_method_names = ['put', 'get']

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
        img = get_object_or_404(Avatar, img=self.kwargs['img'])
        return Response(img.img)

    def put(self, request, *args, **kwargs):
        serializer = UserAvatar
        return Response(status=200)
