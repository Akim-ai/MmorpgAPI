from django.db.models import Manager


class DefaultManager(Manager):
    """
    Only NOT Deleted Model
    """
    def get_queryset(self, deleted: bool = False):
        return super().get_queryset().filter(deleted=deleted)

    def filter(self, deleted: bool = False, *args, **kwargs):
        return super().filter(deleted=deleted, *args, **kwargs)

    def get(self, deleted: bool = False, *args, **kwargs):
        return super().get(deleted=deleted, *args, **kwargs)

    def get_or_create(self, deleted: bool = False, *args, **kwargs):
        instance = super().get_or_create(deleted=deleted, *args, *kwargs)
        return instance


class DeletedManager(Manager):
    """
    Only Deleted Models
    """
    def get_queryset(self, deleted: bool = True):
        return super().get_queryset().filter(deleted=deleted)

    def filter(self, deleted: bool = True, *args, **kwargs):
        return super().filter(deleted=deleted, *args, **kwargs)

    def get(self, deleted: bool = True, *args, **kwargs):
        return super().get(deleted=deleted, *args, **kwargs)

    def get_or_create(self, *args, **kwargs):
        instance = super().get_or_create(*args, *kwargs)
        return instance
