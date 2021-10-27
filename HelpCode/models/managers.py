from django.db import models


class DefaultManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted=False).order_by('create_date')
