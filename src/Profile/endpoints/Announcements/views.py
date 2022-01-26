from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from src.Announcements.models import Announcement, AnnouncementResponse
from src.Announcements.endpoints.serializers import (
    AnnouncementListSerializer,
    AnnouncementResponseListRetrieveSerializer,
)


class SelfAnnouncementList(ListAPIView):

    permission_classes = [IsAuthenticated]
    http_method_names = ('get', )

    def get_queryset(self):
        announcements = Announcement.objects.filter(user=self.request.user)
        return announcements

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return AnnouncementListSerializer
        raise Exception('Method not allowed.')


class SelfAnnouncementResponseList(ListAPIView):

    permission_classes = [IsAuthenticated]
    http_method_names = ('get', )

    def get_queryset(self):
        responses = AnnouncementResponse.objects.filter(
            announcement_id=self.kwargs['pk'], announcement__user=self.request.user
        )
        return responses

    def get_serializer_class(self):
        return AnnouncementResponseListRetrieveSerializer


class SelfResponses(ListAPIView):

    permission_classes = [IsAuthenticated]
    http_method_names = ('get', )

    def get_queryset(self):
        return AnnouncementResponse.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        return AnnouncementResponseListRetrieveSerializer
