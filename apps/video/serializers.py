from rest_framework import serializers

from apps.video.models import (
    Video,
    VideoCategory
)


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'title', 'file_url', 'upload_time', 'author', 'categories']

    file_url = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()
    upload_time = serializers.SerializerMethodField()

    def get_file_url(self, video_obj):
        return video_obj.file.url

    def get_author(self, video_obj):
        return video_obj.author.username

    def get_categories(self, video_obj):
        return video_obj.video_categories.category_name

    def get_upload_time(self, video_obj):
        return video_obj.upload_time.timestamp()


class VideoCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoCategory
        fields = "__all__"
