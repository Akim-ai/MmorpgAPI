from django.conf import settings
from django.urls import path

from .views import (
    AnnouncementListCreateView,
    AnnouncementResponseListCreateView,
    ResponseAcceptView, AnnouncementResponseDetailView,
    AnnouncementDetailView,
    )


urlpatterns = [
    path('', AnnouncementListCreateView.as_view(), name='api-announcement-list-create'),
    path('<int:pk>/', AnnouncementDetailView.as_view(), name='api-announcement-detail'),
    # path(settings.URL_ANNOUNCEMENT_PICTURES, AnnouncementPictureView.as_view(), name='api-announcement-picture'),
    path('<int:pk>/response/', AnnouncementResponseListCreateView.as_view(), name='api-announcement-response'),
    path('<int:pk>/response/<int:res_id>/', AnnouncementResponseDetailView.as_view(),
         name='api-announcement-response-detail'),
]
