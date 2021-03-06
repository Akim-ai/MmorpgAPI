from django.apps import AppConfig


class AnnouncementsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'

    name = 'src.Announcements'
    label = 'announcements'

    verbose_name = 'Объявления'

    def ready(self):
        import src.Announcements.signals
