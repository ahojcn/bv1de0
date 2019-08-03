from django.db import models

# Create your models here.
from apps.users.models import Teacher
from django.contrib import admin


class VideoCategory(models.Model):
    """视频分类"""
    category_name = models.CharField(max_length=32, verbose_name='分类名称')
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')

    class Meta:
        db_table = 'bv_video_category'
        verbose_name = '视频分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.category_name


class Video(models.Model):
    """视频信息"""
    uploader = models.ForeignKey(Teacher, on_delete=None, verbose_name='上传者')
    categories = models.ForeignKey(VideoCategory, on_delete=None, verbose_name='分类')
    title = models.CharField(max_length=128, verbose_name='视频标题', default='未命名')
    video_path = models.FileField(verbose_name='视频地址')
    upload_time = models.DateTimeField(auto_now_add=True, verbose_name='上传时间')

    class Meta:
        db_table = 'bv_video'
        verbose_name = '视频信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


admin.site.register(VideoCategory)
admin.site.register(Video)
