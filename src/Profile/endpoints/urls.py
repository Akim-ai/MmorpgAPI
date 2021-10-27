from django.urls import path
from .views import UserSelfProfileView, UserProfileView, ProfileAvatar


urlpatterns = [
    path('me/', UserSelfProfileView.as_view(), name='my-profile'),
    path('<int:pk>/', UserProfileView.as_view(), name='profile'),
    path('me/avatar/<str:img>/', ProfileAvatar.as_view(), name='profile-avatar'),
]