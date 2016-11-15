# -*- coding:utf-8 -*-
from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import datetime

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
    
    def __unicode__(self):
        return self.title
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return self.url

class KidUser(models.Model):
    kid_user = models.ForeignKey(User)
    address = models.CharField(max_length=200)
    invalid_password_count = models.IntegerField(default=0)
    last_login_date = models.DateTimeField(default=datetime.today())
    gender = models.CharField(max_length=1,default='M')
    birthday = models.CharField(max_length=10,default='2000-01-01')
    class Meta:
        verbose_name = "KidUser"
        verbose_name_plural = "KidUsers"

    def __str__(self):
        return self.kid_user.username


class Favorite(models.Model):
    fav_user = models.ForeignKey(KidUser)
    fav_kid = models.ForeignKey(Kid)  


    