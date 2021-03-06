#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from django.contrib import admin
from kid import views, feed
from django.contrib.auth.views import *
admin.autodiscover()

urlpatterns = [
    url(r'^$', views.home),
    url(r'^schedule/$', views.schedule),
    url(r'^search/$', views.search),
    url(r'^add/$', views.add),
    url(r'^watch/([\%\w|\s]+)/$', views.home),
    url(r'^watch/([\%\w|\s]+)/([\%\w|\s]+)/$', views.home),
    url(r'^delete/(\d+)/$', views.delete,name='delete'),
    url(r'^detail/(\d+)/$', views.detail,name='detail'),
    url(r'^detail/(\d+)/like/$', views.detail_like,name='detail_like'),
    url(r'^detail/(\d+)/favorite/$', views.detail_favorite,name='detail_favorite'),
    url(r'^myfavorite/$', views.myfavorite,name='myfavorite'),
    url(r'^mydelete/(\d+)$', views.mydelete,name='mydelete'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^feed/$', feed.KidFeed()),
    # user
    url(r'^contact/$', views.contact),
    url(r'^login/$', views.login_page), # 'django.contrib.auth.views.login'
    url(r'^logout/$',views.logout_page),
    url(r'^profile/$',views.user_profile_view),
    url(r'^register/$',views.register_page),
    url(r'^register/success/$',views.register_success),
    url(r'^changepassword/$',views.change_password),
    url(r'^resetpassword/$', views.reset_password, name='reset'),
    url(r'^password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm,{'post_reset_redirect':'/login','template_name':'registration/reset_confirm.html'},name='reset_confirm'),
    url(r'^password/done/$', password_reset_complete,{'template_name':'registration/reset_complete.html'},name='reset_complete'),
    url(r'^password/reset/done/$', password_reset_done,name='reset_done'),

]


handler404 = 'kid.views.page_not_found_view'
handler500 = 'kid.views.page_not_found_view'