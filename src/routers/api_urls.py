from django.urls import path, include
from .yasg import urlpatterns as doc_urls


urlpatterns = [
    path('sign-in/', include('src.oauth.endpoints.urls')),
    path('announcement/', include('src.Announcements.endpoints.urls')),
    path('profile/', include('src.Profile.endpoints.urls')),
]

urlpatterns += doc_urls
