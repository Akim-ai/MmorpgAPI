from ..models import Announcement, AnnouncementResponse, AnnouncementPicture
from src.oauth.models import Auth as User

from rest_framework import serializers

from django.conf import settings


class CustomUserSerializer(serializers.ModelSerializer):
    """Users Serializer"""

    class Meta:
        model = User
        fields = '__all__'


class AnnouncementListSerializer(serializers.ModelSerializer):
    """Announcements list serializer"""
    category = serializers.SerializerMethodField(method_name='category_translate')
    responses = serializers.SerializerMethodField(method_name='count_responses')
    title = serializers.SerializerMethodField(method_name='title_slice')
    description = serializers.SerializerMethodField(method_name='description_slice')
    create_date = serializers.SerializerMethodField(method_name='date_format')

    def category_translate(self, obj):
        category_choices = {
            'Та': 'Танк',
            "Хи": "Хил",
            "ДД": "Демедж-Диллер",
            "То": "Торговец",
            "ГМ": "Гилдмастер",
            "Кв": "Квестгивер",
            "Ку": "Кузнец",
            "Ко": "Кожевник",
            "Зе": "Зельевар",
            "МЗ": "Мастер заклинаний"
        }
        return category_choices[f'{obj.category}']

    def count_responses(self, obj):
        return AnnouncementResponse.objects.filter(announcement=obj.id).count()

    def title_slice(self, obj):
        return obj.title[:150]

    def description_slice(self, obj):
        return obj.description[:200]

    def date_format(self, obj):
        return obj.published.strftime("%d/%m/%y")

    class Meta:
        model = Announcement
        exclude = ['deleted', 'user']


class AnnouncementRetrieveSerializer(serializers.ModelSerializer):
    """Announcements retrieve/detail serializer"""
    user = serializers.SlugRelatedField('username', read_only=True)
    category = serializers.SerializerMethodField(method_name='category_translate')
    pictures = serializers.SerializerMethodField(method_name='pictures_path')
    create_date = serializers.SerializerMethodField(method_name='date_format')

    def category_translate(self, obj):
        category_choices = {
            'Та': 'Танк',
            "Хи": "Хил",
            "ДД": "Демедж-Диллер",
            "То": "Торговец",
            "ГМ": "Гилдмастер",
            "Кв": "Квестгивер",
            "Ку": "Кузнец",
            "Ко": "Кожевник",
            "Зе": "Зельевар",
            "МЗ": "Мастер заклинаний"
        }
        return f'{category_choices[obj.category]}'

    def pictures_path(self, obj):
        img = AnnouncementPicture.objects.filter(announcement_id=obj.id, deleted=False)
        if img.exists():
            img_count = img.count()
            path = settings.URL_ANNOUNCEMENT_PICTURES.replace('<int:pk>', f'{obj.id}')
            images_urls = []
            for i in range(1, img_count+1):
                images_urls.append('router/announcement/' + path.replace('<int:img_num>', f'{i}'))
            return f'{images_urls}'
        else:
            return None

    def date_format(self, obj):
        return obj.published.strftime("%d/%m/%y")

    class Meta:
        model = Announcement
        exclude = ['deleted']


class AnnouncementResponseSerializer(serializers.ModelSerializer):

    user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    announcement = serializers.SlugRelatedField(slug_field='title', read_only=True)
    create_date = serializers.DateTimeField(format="%d/%m/%y")

    class Meta:
        model = AnnouncementResponse
        fields = '__all__'


class ResponseCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = AnnouncementResponse
        fields = ['text', 'create_date']

    def create(self, validated_data):
        return AnnouncementResponse.objects.create(**validated_data)


class ResponseUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = AnnouncementResponse
        exclude = ['id', 'accepted', 'user', 'announcement', 'deleted']

    def update(self, instance, validated_data):
        instance.text = validated_data.get('text', instance.text)
        instance.save()
        return instance


class ResponseDestroySerializer(serializers.ModelSerializer):

    class Meta:
        model = AnnouncementResponse
        fields = ['deleted']

    def update(self, instance, validated_data):
        instance.deleted = validated_data.get('deleted', instance.deleted)
        instance.save()
        return instance


class ResponseAcceptSerializer(serializers.ModelSerializer):

    class Meta:
        model = AnnouncementResponse
        fields = ['accepted']

    def update(self, instance, validated_data):
        instance.accepted = validated_data.get('accepted', instance.accepted)
        instance.save()
        return instance


class AnnouncementPictureSerializer(serializers.ModelSerializer):

    class Meta:
        model = AnnouncementPicture
        fields = ['img']
