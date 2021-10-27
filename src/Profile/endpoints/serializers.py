from rest_framework import serializers
from src.oauth.models import Auth as User, Avatar
from src.Announcements.models import Announcement, AnnouncementResponse


class AvatarField(serializers.RelatedField):
    def to_representation(self, value):
        request = self.context.get('request')
        img = value.last()
        if img:
            return request.build_absolute_uri('avatar/' + str(img))
        return None


class ProfileSerializer(serializers.ModelSerializer):

    avatar = AvatarField(many=False, read_only=True)
    display_name = serializers.SerializerMethodField(method_name='get_display_name')

    class Meta:
        model = User
        exclude = ('id', 'join_date', 'email')

    def get_display_name(self, instance):
        if instance.display_name:
            return f'{instance.display_name}'
        return f'{instance.email}'


class ProfileSelfSerializer(ProfileSerializer):

    announcements = serializers.SerializerMethodField(method_name='announcement_count')
    announcement_responses = serializers.SerializerMethodField(method_name='announcement_responses_count')

    def announcement_count(self, instance):
        return f'{Announcement.objects.filter(user=instance).count()}'

    def announcement_responses_count(self, instance):
        return f'{AnnouncementResponse.objects.filter(user=instance).count()}'


class UserAvatar(serializers.ModelSerializer):

    class Meta:
        model = Avatar
        fields = ('img',)

    def create(self, validated_data):
        return Avatar.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.deleted = validated_data.get('image', instance.image)
