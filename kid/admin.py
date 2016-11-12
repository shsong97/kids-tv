# -*- coding:utf-8 -*-
from django.contrib import admin
from kid.models import *


class AdminCategory1(admin.ModelAdmin):
    ordering = ("title",)
    search_fields = ("title",)


class AdminCategory2(admin.ModelAdmin):
    ordering = ("title",)
    search_fields = ("title",)
    list_display = ("title", "parent_category", )


class AdminKid(admin.ModelAdmin):
    search_fields = ("title",)
    list_display = ("title", "category", "url", "update_date", "youtube_id" )
    list_filter = ("category", "update_date", )
    ordering = ("update_date",)

class AdminKidUser(admin.ModelAdmin):
    # search_fields = ("title",)
    list_display = ("kid_user", "address", "invalid_password_count", "last_login_date", )
    # list_filter = ("category", "update_date", )
    # ordering = ("update_date",)

class AdminFavorite(admin.ModelAdmin):
    # search_fields = ("title",)
    list_display = ("fav_user", "fav_kid", )
    # list_filter = ("category", "update_date", )
    # ordering = ("update_date",)

admin.site.register(Category1, AdminCategory1)
admin.site.register(Category2, AdminCategory2)
admin.site.register(Kid, AdminKid)
admin.site.register(KidUser, AdminKidUser)
admin.site.register(Favorite, AdminFavorite)