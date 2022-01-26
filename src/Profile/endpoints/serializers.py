from rest_framework import serializers
from src.oauth.models import Auth as User, Avatar
from src.Announcements.models import Announcement, AnnouncementResponse


class AvatarField(serializers.RelatedField):
    def to_representation(self, value):
        request = self.context.get('request')
        img = value.last()
        print(img.build_url)
        if img:
            return request.build_absolute_uri(img.build_url)
        return None


class ProfileSerializer(serializers.ModelSerializer):

    avatar = AvatarField(many=False, read_only=True)
    name = serializers.SerializerMethodField(method_name='build_username', read_only=True)

    class Meta:
        model = User
        fields = ('avatar', 'bio', 'city', 'country', 'avatar', 'name')

    def build_username(self, instance):
        return f'{instance.show_display_name}'


class ProfileSelfSerializer(ProfileSerializer):

    announcements = serializers.SerializerMethodField(method_name='announcement_count')
    announcement_responses = serializers.SerializerMethodField(method_name='announcement_responses_count')

    def announcement_count(self, instance):
        return f'{Announcement.objects.filter(user=instance).count()}'

    def announcement_responses_count(self, instance):
        return f'{AnnouncementResponse.objects.filter(user=instance).count()}'

    class Meta:
        model = User
        exclude = ('id', 'create_date', 'email', 'is_authenticated', 'password')
        optional_fields = '__all__'


class UserAvatar(serializers.ModelSerializer):

    class Meta:
        model = Avatar
        fields = ('img',)

    def create(self, validated_data):
        return Avatar.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.deleted = validated_data.get('image', instance.image)
