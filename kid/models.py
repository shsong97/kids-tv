# -*- coding:utf-8 -*-
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Category1(models.Model):
    title = models.CharField(max_length=200)

    def __unicode__(self):
        return self.title
        
    def __str__(self):
        return self.title

class Category2(models.Model):
    title = models.CharField(max_length=200)
    parent_category = models.ForeignKey(Category1)

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']
        
class Kid(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField()
    image_url = models.CharField(max_length=400)
    create_date = models.DateTimeField(default=timezone.now)
    update_date =  models.DateTimeField(default=timezone.now)
    category = models.ForeignKey(Category2)
    youtube_id = models.CharField(max_length=100, default='')
    view_count = models.IntegerField(default=0)
    def __unicode__(self):
        return self.title
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return self.url

class KidUser(models.Model):
    kid_user = models.ForeignKey(User)
    address = models.CharField('주소',max_length=200)
    invalid_password_count = models.IntegerField('비밀번호 실패횟수',default=0)
    last_login_date = models.DateTimeField('마지막접속일',default=timezone.now)
    GENDER_CHOICE =(('M','남자'),('F','여자'))
    gender = models.CharField('성별',max_length=1,default='M',choices=GENDER_CHOICE)
    birthday = models.CharField('생년월일',max_length=10,default='2000-01-01')
    class Meta:
        verbose_name = "KidUser"
        verbose_name_plural = "KidUsers"

    def __str__(self):
        return self.kid_user.username


class Favorite(models.Model):
    fav_user = models.ForeignKey(KidUser)
    fav_kid = models.ForeignKey(Kid)  


    