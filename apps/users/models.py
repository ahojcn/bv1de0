# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib import admin
from apps.bclass.models import BClass  # 班级类


class User(AbstractUser):
    """用户基类"""
    avatar = models.ImageField(default='https://b-ssl.duitang.com/uploads/item/201508/28/20150828225753_jJ4Fc.jpeg', verbose_name='头像')
    motto = models.CharField(max_length=256, verbose_name='个性签名')
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')

    class Meta:
        db_table = 'bv_user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name


class Student(User):
    """学生类"""
    the_class = models.ForeignKey(BClass, on_delete=None)

    class Meta:
        db_table = 'bv_student'
        verbose_name = '学生'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class Teacher(User):
    """教师类"""

    class Meta:
        db_table = 'bv_teacher'
        verbose_name = '教师'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


admin.site.register(Student)
admin.site.register(Teacher)
