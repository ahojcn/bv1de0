from rest_framework import serializers

from apps.user.models import User
from apps.video.models import Video


class UserHomeSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()
    video_list = serializers.SerializerMethodField()

    def get_avatar(self, user_obj):
        return user_obj.avatar.url

    def get_video_list(self, user_obj):
        resp_list = []
        for item in Video.objects.filter(author=user_obj):
            temp_json = {
                "title": item.title,
                "file": item.file.url,
                "upload_time": item.upload_time.timestamp(),
                "categories": item.video_categories.category_name
            }
            resp_list.append(temp_json)
        return resp_list

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'nick_name', 'motto',
            'avatar', 'is_active', 'password', 'video_list'
        ]
        read_only_fields = ['id', 'email', 'is_active']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.nick_name = validated_data.get('nick_name', instance.nick_name)
        instance.motto = validated_data.get('motto', instance.motto)
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "nick_name", "avatar", "motto", "date_joined"]

    avatar = serializers.SerializerMethodField()
    date_joined = serializers.SerializerMethodField()

    def get_avatar(self, user_obj):
        return user_obj.avatar.url

    def get_date_joined(self, user_obj):
        return user_obj.date_joined.timestamp()
