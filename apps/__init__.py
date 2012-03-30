#-*- coding: utf-8 -*-
class AdminSite(object):

    def get_urls(self):
        import os
        from django.conf.urls.defaults import patterns, url, include
        from django.conf import settings

        urlpatterns = patterns('',)

        for app in settings.APPS_LIST:
            urlpatterns += patterns('',
                url(r'^%s/' % app, include('%s.urls' % app))
            )
        return urlpatterns

    @property
    def urls(self):
        return self.get_urls()

site = AdminSite()