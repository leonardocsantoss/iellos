# -*- coding:utf-8 -*-
from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

import apps


urlpatterns = patterns('',
    # Example:
    # (r'^base/', include('base.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^', include('account.urls')),
    #URLs of the admin-tools
    url(r'^admin_tools/', include('admin_tools.urls')),
    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    #URLs of the report
    (r'^report/', include('report.urls')),
    (r'^@', include('profiles.urls')),
    (r'^!',include('elos.urls')),
    (r'^posts/', include('posts.urls')),
    (r'^comments/', include('django.contrib.comments.urls')),
    (r'^tagging_autocomplete/', include('tagging_autocomplete.urls')),
    (r'^apps/', include(apps.site.urls)),

)

if settings.LOCAL:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.STATIC_ROOT, 'show_indexes': True}),
        (r'^admin_media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.ADMIN_MEDIA_ROOT, 'show_indexes': True}),
    )