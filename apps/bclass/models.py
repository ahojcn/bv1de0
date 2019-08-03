from django.db import models

# Create your models here.
from django.contrib import admin


class BClass(models.Model):
    """班级类"""
    b_name = models.CharField(max_length=256, verbose_name='班级名')
    b_begin_date = models.DateField(auto_now_add=True, verbose_name='开班时间')
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')

    class Meta:
        db_table = 'bv_class'
        verbose_name = '班级'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.b_name + '班'


admin.site.register(BClass)
