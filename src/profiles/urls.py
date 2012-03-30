from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^foto/upload/$', 'profiles.views.upload_profile_image', name="upload_profile_image"),
    url(r'^pesquisa/$', 'profiles.views.pesquisa', name="pesquisa"),
    url(r'^default/edit/$', 'profiles.views.edit_profile_default', name="edit_profile_default"),
    url(r'^select/apps/(?P<app>[\w\-\_]+)/$', 'profiles.views.select_app', name="select_app"),
    url(r'^add/apps/$', 'profiles.views.add_app', name="add_app"),
    url(r'^(?P<username>\w+)/$', 'profiles.views.profiles', name="profiles"),
)