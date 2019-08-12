from django.db import models


# Create your models here.


# 发布会表
class Event(models.Model):
    name = models.CharField(max_length=100, verbose_name='发布会标题')
    limit = models.IntegerField(verbose_name='参加人数')
    status = models.BooleanField(verbose_name='状态')
    address = models.CharField(max_length=200, verbose_name='地址')
    start_time = models.DateTimeField(verbose_name='发布会时间')
    create_time = models.DateTimeField(auto_now=True, verbose_name='创建时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '发布会表'
        verbose_name_plural = '发布会表'
        ordering = ['-create_time']


# 嘉宾表
class Guest(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name='发布会')
    realname = models.CharField(max_length=64, verbose_name='姓名')
    phone = models.CharField(max_length=20, verbose_name='手机号码')
    email = models.EmailField(verbose_name='邮箱')
    sign = models.BooleanField(verbose_name='签到状态')
    create_time = models.DateTimeField(auto_now=True, verbose_name='创建时间')

    def __str__(self):
        return self.realname

    class Meta:
        unique_together = ('event', 'phone')
        verbose_name_plural = '嘉宾表'
        verbose_name = '嘉宾表'
