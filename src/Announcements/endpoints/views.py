from ..models import Announcement, AnnouncementResponse, AnnouncementPicture

from rest_framework.generics import (ListAPIView, RetrieveAPIView,
                                     UpdateAPIView, CreateAPIView,
                                     DestroyAPIView)
from rest_framework.response import Response
from .custom_renders import JPEGRenderer, PNGRenderer
from .serializers import (
    AnnouncementListSerializer,
    AnnouncementRetrieveSerializer,
    AnnouncementResponseSerializer,
    ResponseUpdateSerializer,
    ResponseCreateSerializer,
    ResponseDestroySerializer,
    ResponseAcceptSerializer,
    AnnouncementPictureSerializer,
)
from rest_framework.pagination import PageNumberPagination

from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.shortcuts import get_object_or_404

"""Image validation"""
from io import BytesIO
from PIL import Image


class AnnouncementRetrieveListView(RetrieveAPIView, ListAPIView):
    """Announcements retrieve/list view"""

    permission_classes = [IsAuthenticated]
    serializer_class = AnnouncementListSerializer

    def get(self, request, *args, **kwargs):
        context = {}
        if kwargs:
            announcement = Announcement.objects.get(id=kwargs['pk'], deleted=False)
            if announcement:
                context['announcement'] = AnnouncementRetrieveSerializer(announcement).data
        else:
            announcement = Announcement.objects.all()
            if announcement:
                context['announcements'] = AnnouncementListSerializer(announcement, many=True).data
        return Response(context)


class AnnouncementResponseListView(ListAPIView):

    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = PageNumberPagination
    serializer_class = AnnouncementResponseSerializer

    def get_queryset(self):
        responses = AnnouncementResponse.objects.filter(announcement_id=self.kwargs['pk'], deleted=False)
        return responses


class AnnouncementResponseCreateView(UpdateAPIView, CreateAPIView):
    """Response Update Create View"""

    http_method_names = ['post']
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        return ResponseCreateSerializer

    def post(self, request, *args, **kwargs):
        if Announcement.objects.filter(id=kwargs['pk'], user=request.user, deleted=False):
            raise Exception("You can't comment announcement created by yourself")
        serializer = self.get_serializer_class()
        serializer = serializer(data=request.data)
        if serializer.is_valid():
            text = serializer.data
            AnnouncementResponse.objects.create(user=request.user,
                                                text=text.get('text', text),
                                                announcement_id=kwargs['pk'])
            return Response(status=200)
        return Response(exception='Data is not valid')


class AnnouncementResponseUpdateCreateView(UpdateAPIView, CreateAPIView):
    """Announcement Response Create Update"""
    
    http_method_names = ['post', 'put']
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ResponseUpdateSerializer
        elif self.request.method == 'PUT':
            return ResponseDestroySerializer

    def get_object(self):
        response = AnnouncementResponse.objects.filter(
            id=self.kwargs['res_id'], user=self.request.user,
            announcement_id=self.kwargs['pk'], deleted=False
        )
        return response

    def action(self, request, *args, **kwargs):
        response = self.get_object()
        serializer = self.get_serializer_class()
        serializer = serializer(response, data=request.data)
        if response and serializer.is_valid():
            serializer.save()
            return Response(status=200)
        return Response(status=404)

    def post(self, request, *args, **kwargs):
        return self.action(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.action(request, *args, **kwargs)


class ResponseAcceptView(UpdateAPIView):
    http_method_names = ['put']
    permission_classes = [IsAuthenticated]
    serializer_class = ResponseAcceptSerializer

    def put(self, request, *args, **kwargs):
        response = get_object_or_404(AnnouncementResponse,
                                     announcement_id=self.kwargs['pk'],
                                     id=self.kwargs['res_id'],
                                     deleted=False,
                                     announcement__user=self.request.user)
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
    permission_classes = [IsAuthenticatedOrReadOnly]

    image_input_formats = ['png', 'jpg', 'jpeg']
    image_min_max_height = [400, 1080]
    image_min_max_width = [400, 1980]

    def get(self, request, *args, **kwargs):
        queryset = AnnouncementPicture.objects.filter(announcement_id=self.kwargs['pk'], deleted=False)
        object_num = int(self.kwargs['img_num'])
        if queryset.count() >= object_num:
            return Response(queryset[object_num - 1].img)
        return Response(status=404)

    def get_object(self):
        img = AnnouncementPicture.objects.filter(announcement_id=self.kwargs['pk'],
                                                 announcement__user=self.request.user,
                                                 user=self.request.user, deleted=False)
        if img.count() >= self.kwargs['img_num']:
            return img[self.kwargs['img_num']-1]
        return ''

    def get_serializer_class(self):
        if self.request.method == 'PUT' or self.request.method == 'POST':
            return AnnouncementPictureSerializer

    def image_validation(self, image):
        if 0 < len(str(image)) < 256:
            if str(image).split('.')[-1] in self.image_input_formats:
                image_size = Image.open(BytesIO(image.read())).size
                if self.image_min_max_height[0] < image_size[1] < self.image_min_max_height[1] \
                        and self.image_min_max_width[0] < image_size[0] < self.image_min_max_width[1]:
                    return True
                else:
                    raise Exception('Invalid image size. Valid height- from {0} to {1}. Valid width- from {2} to {3}'
                                     .format(self.image_min_max_height[0], self.image_min_max_height[1],
                                             self.image_min_max_width[0], self.image_min_max_width[1]))
            else:
                raise Exception('Invalid image format. Allowed formats: ' + ', '.join(self.image_input_formats))
        raise Exception('Name of the image must be less then 225 symbols')

    def post(self, request, *args, **kwargs):
        if self.image_validation(request.data['img']):
            announcement = Announcement.objects.get(id=kwargs['pk'])
            if announcement:
                if announcement.announcementpicture_set.filter(deleted=False).count() <= 10:
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

    def delete(self, request, *args, **kwargs):
        img = self.get_object()
        if img:
            img.deleted = True
            img.save(update_fields=['deleted'])
            return Response(status=200)
        return Response(status=404)
