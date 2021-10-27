from django.urls import path, include


urlpatterns = [
    path('api/v1/', include('src.routers.api_urls')),
    path('sign-in/', include('src.oauth.urls')),
]
