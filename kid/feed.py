# -*- coding:utf-8 -*-
from django.contrib.syndication.views import Feed
from .models import Kid

class KidFeed(Feed):
    title = 'Latest kid items'
    link = '/feed/'
    description = 'Latest 10 kid items'
    description_template = "feed.html"
    
    def items(self):
        return Kid.objects.order_by('-update_date')[:10]
    
    def item_description(self, obj):
        return obj.title