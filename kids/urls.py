#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
from kid import views
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'kid.views.home'),
    url(r'^schedule/$', 'kid.views.schedule'),
    url(r'^search/$', 'kid.views.search'),
    url(r'^add/$', 'kid.views.add'),
    url(r'^watch/([\%\w|\s]+)$', 'kid.views.home'),
    url(r'^watch/([\%\w|\s]+)/([\%\w|\s]+)$', 'kid.views.home'),
    url(r'^admin/', include(admin.site.urls)),
)
