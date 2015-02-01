from django.contrib import admin
from kid.models import *


class AdminCategory1(admin.ModelAdmin):
    ordering = ("title",)
    search_fields = ("title",)


class AdminCategory2(admin.ModelAdmin):
    ordering = ("title",)
    search_fields = ("title",)


class AdminKid(admin.ModelAdmin):
    list_display = ("title", "url", "update_date", )
    list_filter = ("update_date",)
    ordering = ("update_date",)


admin.site.register(Category1, AdminCategory1)
admin.site.register(Category2, AdminCategory2)
admin.site.register(Kid, AdminKid)