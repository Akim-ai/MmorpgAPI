from django.conf import settings
from django.urls import path

from .views import (AnnouncementRetrieveListView, AnnouncementPictureView,
                    AnnouncementResponseListView, AnnouncementResponseCreateView,
                    ResponseAcceptView, AnnouncementResponseUpdateCreateView,)

urlpatterns = [
    path('', AnnouncementRetrieveListView.as_view(), name='announcement-list'),
    path('<int:pk>/', AnnouncementRetrieveListView.as_view(), name='announcement-retrieve'),
    path(settings.URL_ANNOUNCEMENT_PICTURES, AnnouncementPictureView.as_view(), name='announcement-picture'),
    path('<int:pk>/response/', AnnouncementResponseListView.as_view(), name='announcement-responses'),
    # path('<int:pk>/response/<int:res_id>/', AnnouncementResponseUpdateCreateView.as_view(), name='response-update'),
    path('<int:pk>/response-create/', AnnouncementResponseCreateView.as_view(), name='response-create'),
    path('<int:pk>/response-accept/<int:res_id>', ResponseAcceptView.as_view(), name='response-accept'),
]
