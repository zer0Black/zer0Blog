# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class User(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=32)
    name = models.CharField(max_length=12)


class Tag(models.Model):
    name = models.CharField(max_length=20, primary_key=True)


class Post(models.Model):
    title = models.CharField(max_length=100)
    publish_time = models.DateTimeField(auto_now_add=True)  # 第一次保存时自动添加时间
    modify_time = models.DataTimeField(auto_now=True)  # 每次保存自动更新时间
    author = models.ForeignKey(User)
    content = models.TextField()
    tag = models.ManyToManyField(Tag, blank=True, default="", on_delete=models.SET_DEFAULT())  # 外键tag可为空，外键被删除时该值设定为默认值“”
    view_count = models.IntegerField(editable=True, default=0)
    status = models.SmallIntegerField(default=0)  # 0为草稿，1为发布，2为删除


class Comment(models.Model):
    post = models.ForeignKey(Post)
    author = models.ForeignKey(User)
    publish_Time = models.DateTimeField(auto_now_add=True)
    ip_address = models.IPAddressField()
    content = models.CharField(max_length=500)
    isDelete = models.BooleanField(default=False)


