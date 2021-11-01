from django.conf import settings
from django.urls import path

from .views import (
    AnnouncementListCreateView, AnnouncementPictureView,
    AnnouncementResponseListCreateView,
    ResponseAcceptView, AnnouncementResponseDetailView,
    AnnouncementDetailView,
    )


urlpatterns = [
    path('', AnnouncementListCreateView.as_view(), name='announcement-list-create'),
    path('<int:pk>/', AnnouncementDetailView.as_view(), name='announcement-detail'),
    path(settings.URL_ANNOUNCEMENT_PICTURES, AnnouncementPictureView.as_view(), name='announcement-picture'),
    path('<int:pk>/response/', AnnouncementResponseListCreateView.as_view(), name='announcement-response'),
    path('<int:pk>/response/<int:res_id>/', AnnouncementResponseDetailView.as_view(),
          name='announcement-response-detail'),
]
