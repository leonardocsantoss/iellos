# -*- coding:utf-8 -*-
from django.contrib import admin
from models import ProfileImage, ProfileDefault


class ProfileImageAdmin(admin.ModelAdmin):

    list_display = ("user", "image", )
    search_fields = ("user__first_name", "user__last_name", "user__username", "user__email", )


class ProfileDefaultAdmin(admin.ModelAdmin):

    list_display = ("user", )
    search_fields = ("user__first_name", "user__last_name", "user__username", "user__email", )

admin.site.register(ProfileImage, ProfileImageAdmin)
admin.site.register(ProfileDefault, ProfileDefaultAdmin)
