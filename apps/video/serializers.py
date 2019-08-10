from rest_framework import serializers

from apps.video.models import (
    Video,
    VideoCategory
)


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'title', 'file', 'upload_time', 'author', 'video_categories']


class VideoCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoCategory
        fields = "__all__"
