from django.contrib import admin
from .models import (
    Announcement, AnnouncementResponse,
    AnnouncementPicture,
    )


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'user', 'category', 'title',
        'description', 'create_date', 'deleted'
    ]


@admin.register(AnnouncementResponse)
class AnnouncementResponseAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'user', 'text', 'create_date',
        'accepted', 'deleted'
    ]


@admin.register(AnnouncementPicture)
class AnnouncementPictureAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'user', 'announcement', 'img',
        'create_date', 'deleted'
    ]
    list_display_links = [
        'id', 'img'
    ]
