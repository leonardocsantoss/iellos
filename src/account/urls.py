# -*- coding:utf-8 -*-
from django.conf.urls.defaults import *

from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
    url(r'^$', 'account.views.login', name="acct_login"),
    url(r'^registro/$', 'account.views.signup', name="acct_signup"),
    url(r'^alterar/senha/$', 'account.views.password_change', name="acct_passwd"),
    url(r'^criar/senha/$', 'account.views.password_set', name="acct_passwd_set"),
    url(r'^redefinir/senha/$', 'account.views.password_reset', name="acct_passwd_reset"),
    
    url(r'^linguagem/$', 'account.views.language_change', name="acct_language_change"),
    url(r'^sair/$', 'django.contrib.auth.views.logout', {"next_page": "/"}, name="acct_logout"),
    
    url(r'^confirmar/email/(\w+)/$', 'emailconfirmation.views.confirm_email', name="acct_confirm_email"),

    # Setting the permanent password after getting a key by email
    url(r'^alerar/senha/key/(\w+)/$', 'account.views.password_reset_from_key', name="acct_passwd_reset_key"),


    url(r'^termos-de-uso/$', direct_to_template, {'template': 'account/termos_de_uso.html'}, name="termos_de_uso"),
    url(r'^politica-de-privacidade/$', direct_to_template, {'template': 'account/politica_de_privacidade.html'}, name="politica_de_privacidade"),
)
