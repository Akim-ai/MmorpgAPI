from django.conf import settings
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend, filters
from rest_framework.generics import (
    ListAPIView, RetrieveAPIView,
    UpdateAPIView, CreateAPIView,
    DestroyAPIView,
)

from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from utils.permissions import IsOwnerOrReadOnly, IsOwner

from rest_framework.response import Response

from .custom_renders import JPEGRenderer, PNGRenderer
from .serializers import (
    AnnouncementListSerializer,
    AnnouncementRetrieveSerializer,
    AnnouncementResponseListRetrieveSerializer,
    AnnouncementResponseUpdateSerializer,
    AnnouncementResponseCreateSerializer,
    ResponseAcceptSerializer,
    AnnouncementPictureSerializer,
    AnnouncementUpdateSerializer,
    AnnouncementCreateSerializer,
)
from ..models import Announcement, AnnouncementResponse, AnnouncementPicture

"""Image validation"""
from io import BytesIO
from PIL import Image

"""Filters"""
from .filters import AnnouncementListFilter


class AnnouncementListCreateView(ListAPIView, CreateAPIView):
    """Announcements list create view"""

    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = AnnouncementListFilter

    def get_queryset(self):
        return Announcement.objects.all()

    def get_serializer_class(self):
        return AnnouncementListSerializer

    def get_serializer(self, queryset, *args, **kwargs):

        serializer = self.get_serializer_class()
        if self.request.method == 'POST':
            data = self.request.data
            return serializer(
                data={**data},
                context={'user': self.request.user}
            )

        serializer = serializer(data=queryset, many=True)
        if serializer.is_valid():
            return serializer
        return serializer

    def list(self, request, *args, **kwargs):
        response = super().list(request, args, kwargs)
        response.data['paginated_by'] = settings.REST_FRAMEWORK['PAGE_SIZE']
        return response


class AnnouncementDetailView(RetrieveAPIView, UpdateAPIView, DestroyAPIView):
    """Announcement Retrieve, Update, Destroy"""
    permission_classes = [IsAuthenticated]
    serializer_class = AnnouncementRetrieveSerializer
    http_method_names = ['get', 'put', 'delete']

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == 'GET':
            return AnnouncementRetrieveSerializer
        elif self.request.method == 'PUT':
            return AnnouncementUpdateSerializer
        else:
            raise Exception(f'Method {self.request.method} is not allowed')

    def get_queryset(self):
        announcement = Announcement.objects.get(id=self.kwargs['pk'])
        return announcement

    def get_object(self):
        return self.get_queryset()


class AnnouncementResponseListCreateView(ListAPIView, CreateAPIView):
    """
    Self Created Announcement Resnpose List Create View
    """

    http_method_names = ['get', 'post']
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        responses = AnnouncementResponse.objects.filter(announcement_id=self.kwargs.get('pk'))
        return responses

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AnnouncementResponseCreateSerializer
        if self.request.method == "GET":
            return AnnouncementResponseListRetrieveSerializer

    def perform_create(self, serializer):
        AnnouncementResponse.objects.create(
            user=self.request.user, announcement=Announcement.objects.get(id=self.kwargs.get('pk', None)),
            text=serializer.data.get('text', None)
        )
        return


class AnnouncementResponseDetailView(UpdateAPIView, RetrieveAPIView, DestroyAPIView):
    """Announcement Response Create Update"""
    
    http_method_names = ['get', 'put', 'delete']
    permission_classes = [IsAuthenticated, IsOwner]

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return AnnouncementResponseUpdateSerializer
        elif self.request.method == 'GET':
            return AnnouncementResponseListRetrieveSerializer

    def get_object(self):
        response = AnnouncementResponse.objects.get(
            id=self.kwargs['res_id'], user=self.request.user,
            announcement_id=self.kwargs.get('pk', None)
        )
        return response


class ResponseAcceptView(UpdateAPIView):
    http_method_names = ['put']
    permission_classes = [IsAuthenticated]
    serializer_class = ResponseAcceptSerializer

    def put(self, request, *args, **kwargs):
        response = get_object_or_404(
            AnnouncementResponse, announcement_id=self.kwargs['pk'],
            id=self.kwargs['res_id'], announcement__user=self.request.user
        )
        serializer = self.serializer_class
        serializer = serializer(response, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=200)
        return Response(status=404)


class AnnouncementPictureView(RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView):
    """Announcements picture Retrieve view"""

    renderer_classes = [PNGRenderer, JPEGRenderer]
    http_method_names = ['get', 'post', 'put', 'delete']
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    image_input_formats = ['png', 'jpg', 'jpeg']
    image_min_max_height = [400, 1080]
    image_min_max_width = [400, 1980]

    def get(self, request, *args, **kwargs):
        queryset = AnnouncementPicture.objects.filter(
            announcement_id=self.kwargs['pk'],
            deleted=False
        )
        object_num = int(self.kwargs['img_num'])
        if queryset.count() >= object_num:
            return Response(queryset[object_num - 1].img)
        return Response(status=404)

    def get_object(self):
        img = AnnouncementPicture.objects.filter(
            announcement_id=self.kwargs['pk'],
            user=self.request.user, deleted=False
        )
        if img.count() >= self.kwargs['img_num']:
            return img[self.kwargs['img_num']-1]
        raise Exception('There is no object.')

    def get_serializer_class(self):
        if self.request.method == 'PUT' or self.request.method == 'POST':
            return AnnouncementPictureSerializer

    def image_validation(self, image):
        if 0 < len(str(image)) > 254:
            raise Exception('Name of the image must be less then 255 symbols')
        if str(image).split('.')[-1] not in self.image_input_formats:
            raise Exception('Invalid image format. Allowed formats: ' + ', '.join(self.image_input_formats))
        image_size = Image.open(BytesIO(image.read())).size
        if image_size[1] < self.image_min_max_height[0] or image_size[1] > self.image_min_max_height[1] \
                and image_size[0] < self.image_min_max_width[0] or image_size[0] > self.image_min_max_width[1]:
            raise Exception('Invalid image size. Valid height- from {0} to {1}. Valid width- from {2} to {3}'
                            .format(self.image_min_max_height[0], self.image_min_max_height[1],
                                    self.image_min_max_width[0], self.image_min_max_width[1]))
        return True

    def post(self, request, *args, **kwargs):
        if self.image_validation(request.data['img']):
            announcement = Announcement.objects.get(id=kwargs['pk'])
            if announcement:
                if announcement.pictures.all().count() <= 10:
                    AnnouncementPicture.objects.create(user=request.user, announcement=announcement,
                                                       img=request.data['img'])
                    return Response(status=201)
                else:
                    raise Exception('Too much pictures to one announcement. Please delete pictures then add.')
            raise Exception('Incorrect announcement')
        return Response(status=404)

    def put(self, request, *args, **kwargs):
        if self.image_validation(request.data['img']):
            picture = self.get_object()
            if picture:
                AnnouncementPicture.objects.create(user=picture.user, announcement=picture.announcement,
                                                   img=picture.img, deleted=True)
                picture.img = request.data['img']
                picture.save()
                return Response(status=200)
        return Response(status=404)

