from django.db import models
import datetime
from django.utils import timezone

# Create your models here.
class Category1(models.Model):
    title = models.CharField(max_length=200)
    def __unicode__(self):
        return self.title

class Category2(models.Model):
    title = models.CharField(max_length=200)
    parent_category = models.ForeignKey(Category1)
    def __unicode__(self):
        return self.title


class Kid(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField()
    image_url = models.CharField(max_length=400)
    create_date = models.DateTimeField(default=timezone.now)
    update_date =  models.DateTimeField(default=timezone.now)
    category = models.ForeignKey(Category2)
    def __unicode__(self):
        return self.title
