from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):
    """
    用户模型类
    """
    nick_name = models.CharField(verbose_name="昵称", max_length=32, default="", null=True, blank=True)
    avatar = models.ImageField(verbose_name="用户头像", upload_to="media/img/avatar/%Y/%m", blank=True, null=True)
    motto = models.CharField(verbose_name="个性签名", max_length=256, default="这个人很懒，啥都没写。")
    phone = models.CharField(verbose_name="手机号", max_length=16, null=True)
    qq = models.CharField(verbose_name="QQ号", max_length=16, null=True)
    birthday = models.DateTimeField(verbose_name="生日", null=True, blank=True)
    gender = models.CharField(verbose_name="性别",
                              choices=(("male", "男"), ("female", "女")),
                              max_length=8,
                              default="female")

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
