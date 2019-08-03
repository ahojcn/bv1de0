from django.db import models

# Create your models here.
from apps.users.models import Student
from apps.video.models import Video
from django.contrib import admin


class MsgBoard(models.Model):
    """视频留言板"""
    stu = models.ForeignKey(Student, on_delete=None, verbose_name='留言的学生')
    video = models.ForeignKey(Video, on_delete=None, verbose_name='哪一个视频')
    content = models.TextField(max_length=2048, verbose_name='留言内容')

    class Meta:
        db_table = 'bv_msg_board'
        verbose_name = '留言'
        verbose_name_plural = '留言'

    def __str__(self):
        return self.content


admin.site.register(MsgBoard)
