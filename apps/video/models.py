import time

from django.db import models

from apps.user.models import User


class VideoCategory(models.Model):
    """
    视频分类
    """
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name="拥有者")
    category_name = models.CharField(max_length=16, verbose_name="分类名")

    class Meta:
        db_table = "bv_video_category"
        verbose_name = "视频分类"
        verbose_name_plural = "视频分类"

    def __str__(self):
        return self.category_name


class Video(models.Model):
    """
    视频信息
    """

    def video_upload_path(self, filename):
        return self.author.username + "/videos/" + str(time.time()) + filename

    author = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name="视频作者")
    title = models.CharField(max_length=128, verbose_name="视频标题")
    file = models.FileField(upload_to=video_upload_path, verbose_name="视频文件")
    upload_time = models.DateTimeField(auto_now_add=True, verbose_name="上传日期")

    video_categories = models.ForeignKey(to=VideoCategory, on_delete=models.CASCADE, verbose_name="视频分类")

    class Meta:
        db_table = "bv_video"
        verbose_name = "视频"
        verbose_name_plural = "视频"

    def __str__(self):
        return self.title
