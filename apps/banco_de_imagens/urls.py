from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$','banco_de_imagens.views.index', name="bi_index"),
    url(r'^adicionar/$','banco_de_imagens.views.adicionar', name="bi_adicionar"),
    url(r'^scroll/(?P<page>\d+)/$', 'banco_de_imagens.views.index_scroll', name="bi_index_scroll"),
    url(r'^imagem/(?P<slug>[\w-]+)/$','banco_de_imagens.views.imagem', name="bi_imagem"),
    url(r'^imagem/excluir/(?P<slug>[\w-]+)/$','banco_de_imagens.views.imagem_excluir', name="bi_imagem_excluir"),
    url(r'^imagem/editar/(?P<slug>[\w-]+)/$','banco_de_imagens.views.imagem_editar', name="bi_imagem_editar"),
    url(r'^imagem/tags/(?P<slug>[\w-]+)/$','banco_de_imagens.views.imagem_tags', name="bi_imagem_tags"),
)
