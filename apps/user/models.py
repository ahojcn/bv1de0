import time

from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class User(AbstractUser):
    """
    用户模型类
    """

    def avatar_upload_path(self, filename):
        return self.username + "/avatars/" + str(time.time()) + filename

    # TODO default avatar 随机一个头像

    nick_name = models.CharField(verbose_name="昵称", max_length=32, default="", null=True, blank=True)
    avatar = models.ImageField(verbose_name="用户头像", upload_to=avatar_upload_path, blank=True, null=True,
                               default="img/avatars/default_avatar.png")
    motto = models.CharField(verbose_name="个性签名", max_length=256, default="这个人很懒，啥都没写。")
    phone = models.CharField(verbose_name="手机号", max_length=16, null=True, blank=True)
    qq = models.CharField(verbose_name="QQ号", max_length=16, null=True, blank=True)
    birthday = models.DateTimeField(verbose_name="生日", null=True, blank=True)
    gender = models.CharField(verbose_name="性别",
                              choices=(("male", "男"), ("female", "女")),
                              max_length=8,
                              default="female")

    class Meta:
        db_table = "bv_user"
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class UserToken(models.Model):
    """
    user token 类
    """
    key = models.CharField(max_length=128, verbose_name="token_key")
    user = models.OneToOneField(User, related_name="auth_token", on_delete=models.CASCADE, verbose_name="所属用户")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        db_table = "bv_user_token"

    def __str__(self):
        return self.key
