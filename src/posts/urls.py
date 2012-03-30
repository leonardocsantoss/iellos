from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^user/$', 'posts.views.user_posts', name="user_posts"),
    url(r'^user/scroll/(?P<page>\d+)/$', 'posts.views.user_posts_scroll', name="user_posts_scroll"),
    url(r'^(?P<slug>[\w_-]+)/scroll/(?P<page>\d+)/$', 'posts.views.elo_posts_scroll', name="elo_posts_scroll"),
    url(r'^delete/(?P<post_id>\d+)/$', 'posts.views.delete_ajax', name='delete_ajax'),
    url(r'^comment/delete/(?P<comment_id>\d+)/$', 'posts.views.delete_comment_ajax', name="delete_comment_ajax"),
)
