from django.conf.urls.defaults import *
from models import *

urlpatterns = patterns('',
    url(r'^criar/$','elos.views.criar', name="elo_criar"),
    url(r'^(?P<slug>[\w-]+)/$', 'elos.views.elo', name="elo"),
    url(r'usuarios/(?P<slug>[\w-]+)/$', 'elos.views.usuarios_elo', name="usuarios_elo"),
    url(r'sair/(?P<slug>[\w-]+)/$', 'elos.views.sair_elo', name="sair_elo"),
    url(r'conectar/(?P<slug>[\w-]+)/$', 'elos.views.conectar_elo', name="conectar_elo"),
    url(r'convidar/(?P<slug>[\w-]+)/$', 'elos.views.convidar_user_elo', name="convidar_user_elo"),
    url(r'votar/(?P<username>\w+)/(?P<slug>[\w-]+)/$', 'elos.views.votar_elo', name="votar_elo"),
    url(r'^all/(?P<page>\d*)/$', 'elos.views.all_elos', name="all_elos"),
)
