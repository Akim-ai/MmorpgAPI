from django.db.models import Manager


class DefaultManager(Manager):
    """
    Default Model Manager
    """
    def get_queryset(self, deleted=False):
        return super().get_queryset().filter(deleted=deleted)

    def filter(self, deleted=False, *args, **kwargs):
        return super().filter(deleted=deleted, *args, **kwargs)

    def get(self, deleted=False, *args, **kwargs):
        return super().get(deleted=deleted, *args, **kwargs)

    def get_or_create(self, *args, **kwargs):
        instance = super().get_or_create(*args, *kwargs)
        return instance


class DeletedManager(Manager):
    """
    Default Model Manager
    """
    def get_queryset(self, deleted=True):
        return super().get_queryset().filter(deleted=deleted)

    def filter(self, deleted=True, *args, **kwargs):
        return super().filter(deleted=deleted, *args, **kwargs)

    def get(self, deleted=True, *args, **kwargs):
        return super().get(deleted=deleted, *args, **kwargs)

    def get_or_create(self, *args, **kwargs):
        instance = super().get_or_create(*args, *kwargs)
        return instance
