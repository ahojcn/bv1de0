from django.db import models


# Create your models here.

class VideoCategory(models.Model):
    """
    视频分类
    """
    category_name = models.CharField(max_length=16, verbose_name="分类名")

    class Meta:
        verbose_name = "视频分类"
        verbose_name_plural = "视频分类"


class Video(models.Model):
    """
    视频信息
    """
    author = models.ForeignKey(to="user.User", on_delete=models.CASCADE, verbose_name="视频作者")
    title = models.CharField(max_length=128, verbose_name="视频标题")
    file = models.FileField(upload_to="MEDIA/video/", verbose_name="视频文件")
    upload_time = models.DateTimeField(auto_now_add=True, verbose_name="上传日期")

    video_categories = models.ForeignKey(to="video.VideoCategory", on_delete=models.CASCADE, verbose_name="视频分类")

    class Meta:
        verbose_name = "视频"
        verbose_name_plural = "视频"
