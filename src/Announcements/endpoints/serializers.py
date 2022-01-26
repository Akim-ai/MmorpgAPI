from rest_framework.reverse import reverse

from ..models import Announcement, AnnouncementResponse, AnnouncementPicture
from src.oauth.models import Auth as User

from rest_framework import serializers

from django.conf import settings


class CustomUserSerializer(serializers.ModelSerializer):
    """Users Serializer"""

    class Meta:
        model = User
        fields = '__all__'


TO_REPRESENTATION_CATEGORY_CHOICES = {
    'Та': 'Танк',
    "Хи": "Хил",
    "ДД": "Демедж Диллер",
    "То": "Торговец",
    "ГМ": "Гилдмастер",
    "Кв": "Квестгивер",
    "Ку": "Кузнец",
    "Ко": "Кожевник",
    "Зе": "Зельевар",
    "МЗ": "Мастер Заклинаний"
}


CREATE_CATEGORY_CHOICES = {
    'Танк': 'Та',
    "Хил": "Хи",
    "Демедж Диллер": "ДД",
    "Торговец": "То",
    "Гилдмастер": "ГМ",
    "Квестгивер": "Кв",
    "Кузнец": "Ку",
    "Кожевник": "Ко",
    "Зельевар": "Зе",
    "Мастер Заклинаний": "МЗ"
}


class AnnouncementListSerializer(serializers.ModelSerializer):
    """Announcements list serializer"""

    title = serializers.CharField(max_length=150)
    description = serializers.CharField(max_length=1500)
    category = serializers.ChoiceField(choices=CREATE_CATEGORY_CHOICES)
    create_date = serializers.DateTimeField(format='%Y-%m-%d %H:%M', read_only=True)

    class Meta:
        model = Announcement
        exclude = ('deleted', 'user')

    def to_representation(self, instance):

        data: dict
        data = super().to_representation(instance)

        data['responses'] = AnnouncementResponse.objects.filter(announcement=instance.id).count()
        data['description'] = instance.description[:200]
        data['category'] = TO_REPRESENTATION_CATEGORY_CHOICES[f'{instance.category}']
        return data

    def create(self, validated_data):

        data: dict
        data = validated_data
        data['category'] = CREATE_CATEGORY_CHOICES[data['category']]

        data['user'] = self.context.get('user')

        return Announcement.objects.create(**data)


class AnnouncementPictureSerializer(serializers.ModelSerializer):

    class Meta:
        model = AnnouncementPicture
        fields = ['img']


class AnnouncementRetrieveUserSerializer(serializers.ModelSerializer):

    name = serializers.SerializerMethodField(method_name='user_name', read_only=True)

    class Meta:
        model = User
        fields = ('name', 'id')

    def user_name(self, instance):
        return f'{instance.show_display_name}'


class AnnouncementRetrieveSerializer(serializers.ModelSerializer):
    """Announcements retrieve/detail serializer"""
    user = AnnouncementRetrieveUserSerializer()
    category = serializers.SerializerMethodField(method_name='category_translate')
    # pictures = serializers.SerializerMethodField(method_name='pictures_path')
    create_date = serializers.DateTimeField(format='%Y-%m-%d %H:%M', read_only=True)

    class Meta:
        model = Announcement
        exclude = ('deleted',)

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
                images_urls.append('api/v1/announcement/' + path.replace('<int:img_num>', f'{i}'))
            return f'{images_urls}'
        else:
            return None
    #
    # def create(self, validated_data):
    #
    #     data: dict
    #     data = validated_data
    #     data['category'] = CREATE_CATEGORY_CHOICES[data['category']]
    #
    #     data['user'] = self.context.get('user')
    #
    #     return Announcement.objects.create(**data)


class AnnouncementUpdateSerializer(serializers.ModelSerializer):

    user = serializers.SlugRelatedField('show_display_name', read_only=True)

    class Meta:
        model = Announcement
        fields = ('title', 'description', 'category', 'user')


class AnnouncementCreateSerializer(serializers.ModelSerializer):

    id = serializers.ReadOnlyField()
    user = serializers.SlugRelatedField('show_display_name', read_only=True)
    category = serializers.ChoiceField(choices=CREATE_CATEGORY_CHOICES)

    class Meta:
        model = Announcement
        fields = ('title', 'description', 'category', 'user', 'id')

    def create(self, validated_data):

        data: dict
        data = validated_data
        data['category'] = CREATE_CATEGORY_CHOICES[data['category']]

        data['user'] = self.context.get('user')

        return Announcement.objects.create(**data)

    def to_representation(self, instance):

        data = super().to_representation(instance)
        data['category'] = TO_REPRESENTATION_CATEGORY_CHOICES[data['category']]

        return data


class AnnouncementResponseListRetrieveSerializer(serializers.ModelSerializer):

    user = serializers.SlugRelatedField(slug_field='show_display_name', read_only=True, required=False)
    create_date = serializers.DateTimeField(format='%Y-%m-%d %H:%M', read_only=True)

    announcement = serializers.SlugRelatedField(slug_field='title', read_only=True)
    announcement_url = serializers.SerializerMethodField(method_name='build_announcement_url')

    class Meta:
        model = AnnouncementResponse
        exclude = ('deleted',)

    def build_announcement_url(self, obj):
        return f'{settings.INDEX_URL}/api/v1/announcement/{obj.id}'


class AnnouncementResponseUpdateSerializer(AnnouncementResponseListRetrieveSerializer):

    user = serializers.SlugRelatedField('show_display_name', read_only=True)
    announcement = serializers.SlugRelatedField('id', read_only=True)

    class Meta:
        model = AnnouncementResponse
        exclude = ('deleted', 'accepted', 'id', )

    def update(self, instance, validated_data):
        instance.text = validated_data.get('text', instance.text)
        instance.save()
        return instance


class AnnouncementResponseCreateSerializer(serializers.ModelSerializer):

    user = serializers.SlugRelatedField('show_display_name', read_only=True)
    announcement = serializers.SlugRelatedField('id', read_only=True)

    class Meta:
        model = AnnouncementResponse
        fields = ('text', 'user', 'announcement')
        # exclude = ('deleted', 'accepted', 'id', )

    def create(self, validated_data):
        return AnnouncementResponse.objects.create(
            **validated_data, user=self.context.get('user'),
            announcement=self.context.get('announcement')
        )


class ResponseAcceptSerializer(serializers.ModelSerializer):

    class Meta:
        model = AnnouncementResponse
        fields = ['accepted']

    def update(self, instance, validated_data):
        instance.accepted = validated_data.get('accepted', instance.accepted)
        instance.save()
        return instance

