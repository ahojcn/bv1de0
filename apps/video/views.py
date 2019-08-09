from rest_framework import viewsets
from rest_framework.response import Response

from apps.video.serializers import VideoSerializer
from apps.video.models import (
    Video,
    VideoCategory
)


class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

    def __init__(self, **kwargs):
        self._res_data = {"status": -2, "msg": "未知错误", "data": []}
        super().__init__(**kwargs)

    def list(self, request, *args, **kwargs):
        for obj in Video.objects.all():
            item = {
                "id": obj.id,
                "author": obj.author.username,
                "video_categories": obj.video_categories.category_name,
                "title": obj.title,
                "file": obj.file.url,
                "upload_time": obj.upload_time
            }
            self._res_data["data"].append(item)

        self._res_data["status"] = 0
        self._res_data["msg"] = "所有视频"
        return Response(self._res_data)
