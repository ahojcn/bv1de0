from django.db import models


# Create your models here.

class Comment(models.Model):
    """
    用户评论
    """
    user = models.ForeignKey(to="user.User", null=False, blank=False, default="", on_delete=models.CASCADE, verbose_name="用户")
    video_to = models.ForeignKey(to="video.Video",default="", on_delete=models.CASCADE, verbose_name="评论的视频")
    detail = models.TextField(max_length=2048, null=True, blank=True, verbose_name="内容")
    add_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="时间")

    class Meta:
        verbose_name = "评论"
        verbose_name_plural = "评论"

    def __str__(self):
        return self.detail[:128]
