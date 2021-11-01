from django.apps import AppConfig


class OauthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'

    name = 'src.oauth'
    app_label = 'oauth'

    verbose_name = 'Авторизованные пользователи'
