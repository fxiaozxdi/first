from django.contrib import admin

from . import models


class UserAdmin(admin.ModelAdmin):
    # 列表时显示的属性
    list_display = ["name", "nickname", "age", "birthday", "password"]
    # 列表时过滤字段
    list_filter = ("name", "age", "password")
    # 进行分页，每页2条数据
    # list_per_page = 2

    # list_editable = ["nickname", "age"]

    list_display_links = ["age", "nickname"]

    # fields = ["name", "nickname", "age"]

    fieldsets = [
        ("base", {"fields": ["age", "header"]}),
        ("other", {"fields": ["name", "nickname"]}),
    ]


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Article)

