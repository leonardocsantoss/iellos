# -*- coding:utf-8 -*-
from django.contrib import admin
from models import Post


class PostAdmin(admin.ModelAdmin):

    list_display = ("user", "data_de_criacao", )
    search_fields = ("user__first_name", "user__last_name", "user__username", "user__email", "text", )


admin.site.register(Post, PostAdmin)

