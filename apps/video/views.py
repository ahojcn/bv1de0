from django.conf import settings

from rest_framework import viewsets
from rest_framework.response import Response

from apps.video.serializers import (
    VideoSerializer,
    VideoCategorySerializer
)
from apps.video.models import (
    Video,
    VideoCategory
)
from apps.user.models import (
    User,
    UserToken,
)


class VideoCategoryViewSet(viewsets.ModelViewSet):
    queryset = VideoCategory.objects.all()
    serializer_class = VideoCategorySerializer

    def __init__(self, **kwargs):
        self._res_data = {"status": -2, "msg": "未知错误", "data": []}
        super().__init__(**kwargs)

    def list(self, request, *args, **kwargs):
        for i in VideoCategory.objects.all():
            temp_json = {
                "id": i.id,
                "category_name": i.category_name,
                "owner": i.owner.username
            }
            self._res_data["data"].append(temp_json)
        self._res_data["status"] = 0
        self._res_data["msg"] = "所有分类"
        super().list(request)
        return Response(self._res_data)

    def retrieve(self, request, *args, **kwargs):
        category_obj = VideoCategory.objects.filter(id=kwargs["pk"]).first()
        if category_obj is None:
            self._res_data["status"] = -1
            self._res_data["msg"] = "没有这个分类"
            self._res_data["data"] = None
            return Response(self._res_data)

        self._res_data["status"] = 0
        self._res_data["msg"] = ""
        self._res_data["data"] = {
            "id": category_obj.id,
            "category_name": category_obj.category_name,
            "owner": category_obj.owner.username
        }
        return Response(self._res_data)


class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

    def __init__(self, **kwargs):
        self._res_data = {"status": -2, "msg": "未知错误", "data": []}
        super().__init__(**kwargs)

    def list(self, request, *args, **kwargs):
        for obj in Video.objects.all().order_by("-upload_time"):
            item = {
                "id": obj.id,
                "author": obj.author.username,
                "categories": obj.video_categories.category_name,
                "title": obj.title,
                "file": obj.file.url,
                "upload_time": int(obj.upload_time.timestamp())
            }
            self._res_data["data"].append(item)

        self._res_data["status"] = 0
        self._res_data["msg"] = "所有视频"
        return Response(self._res_data)

    def create(self, request, *args, **kwargs):
        """
        title, author, video_categories, file
        """
        title = request.data.get("title")
        author_id = request.data.get("author")
        category_id = request.data.get("video_categories")
        f = request.FILES.get("file")

        if not all([title, author_id, category_id, f]):
            self._res_data["status"] = -1
            self._res_data["msg"] = "参数不够"
            self._res_data["data"] = None
            return Response(self._res_data)

        category_obj = VideoCategory.objects.filter(id=category_id).first()
        author_obj = User.objects.filter(id=author_id).first()

        file_path = settings.MEDIA_ROOT + "/video/" + author_obj.username + f.name
        with open(file_path, "wb") as video:
            for v in f.chunks():
                video.write(v)
        Video.objects.create(title=title, author=author_obj, video_categories=category_obj, file=f)

        self._res_data["status"] = 0
        self._res_data["msg"] = "上传成功"
        self._res_data["data"] = {
            "title": title,
            "author": author_obj.username,
            "category": category_obj.category_name,
            "file": settings.MEDIA_URL + "/video/" + author_obj.username + f.name
        }
        return Response(self._res_data)

    def retrieve(self, request, *args, **kwargs):
        video_id = kwargs["pk"]
        video_obj = Video.objects.filter(id=video_id).first()

        if video_obj is None:
            self._res_data["status"] = -1
            self._res_data["msg"] = "无此数据"
            self._res_data["data"] = None
            return Response(self._res_data)

        self._res_data["data"] = {
            "id": video_obj.id,
            "title": video_obj.title,
            "file": video_obj.file.url,
            "upload_time": int(video_obj.upload_time.timestamp()),
            "author": video_obj.author.username,
            "categories": video_obj.video_categories.category_name
        }
        return Response(self._res_data)