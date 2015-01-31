#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
from kid import views
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'kid.views.home'),
    url(r'^(\w+)$', 'kid.views.category1'),
    url(r'^(\w+)/(\w+)$', 'kid.views.category2'),
    url(r'^admin/', include(admin.site.urls)),
)
