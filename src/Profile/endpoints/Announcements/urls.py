from django.urls import path
from .views import SelfAnnouncementList, SelfAnnouncementResponseList

urlpatterns = [
    path('', SelfAnnouncementList.as_view(), name='api-profile-me-announcements'),
    path('<int:pk>/response/', SelfAnnouncementResponseList.as_view(), name='api-profile-me-responses'),
]