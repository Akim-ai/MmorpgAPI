from django.urls import path, include
from .views import UserProfileView, ProfileAvatar


urlpatterns = [
    path('<int:pk>/', UserProfileView.as_view(), name='api-profile'),
    path('avatar/<str:img>/', ProfileAvatar.as_view(), name='api-profile-avatar'),
    # path('announcement/', include('src.Profile.endpoints.Announcements.urls'))
]