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


admin.site.register(Category1, AdminCategory1)
admin.site.register(Category2, AdminCategory2)
admin.site.register(Kid, AdminKid)