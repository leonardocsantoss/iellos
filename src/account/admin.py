# -*- coding:utf-8 -*-
from django.contrib import admin
from account.models import Account, PasswordReset

admin.site.register(Account)

class PasswordResetAdmin(admin.ModelAdmin):
    list_display = ('user', 'temp_key', 'timestamp', 'reset')


admin.site.register(PasswordReset, PasswordResetAdmin)