from django.urls import path, include

from .Announcements.views import SelfResponses
from .views import UserSelfProfileView, ProfileAvatar

urlpatterns = [
	path('', UserSelfProfileView.as_view(), name='api-profile-me'),
	path('announcement/', include('src.Profile.endpoints.Announcements.urls')),
	path('avatar/<str:img>/', ProfileAvatar.as_view(), name='api-profile-avatar'),
	path('responses/', SelfResponses.as_view(), name='api-self-responses'),
]