from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import AnnouncementResponse

from .tasks import send_response_create_mail, send_response_accept_mail


@receiver(post_save, sender=AnnouncementResponse)
def response_create_send_mail(sender, instance, created, **kwargs):
    if created:
        send_response_create_mail.delay(email=instance.user.email)
    return


@receiver(pre_save, sender=AnnouncementResponse)
def response_accept_send_mail(sender, instance, **kwargs):
    if not instance.id:
        return
    if instance.accepted and not AnnouncementResponse.objects.get(id=instance.id).accepted:
        send_response_accept_mail.delay(email=instance.user.email)
    return
