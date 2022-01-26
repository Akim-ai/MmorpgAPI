from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include


urlpatterns = [
    path('sign-in/', include('src.oauth.urls')),
    path('announcement/', include('src.Announcements.urls')),
    path('profile/', include('src.Profile.urls')),
    path(f'{settings.API_AND_VERSION}', include('src.routers.api_urls'), name='api'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
