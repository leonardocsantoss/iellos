# -*- coding:utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django import template
from elos.models import Elo
from django.core.urlresolvers import reverse
from easy_thumbnails.files import get_thumbnailer

register = template.Library()



@register.simple_tag
def get_elos(user):
    elos = Elo.objects.filter(membros=user)
    retorno = u''
    if len(elos):
        for elo in elos:
            retorno += u'<h2><a href="%s">%s</a></h2>' % (elo.get_absolute_url(), elo.nome)
    else:
        retorno += u'<h2>%s</h2>' % _(u'Você não tem nenhum elo!')
    return retorno



@register.simple_tag
def elos_image(users, max, tam):
    retorno = u""
    if len(users) >= max:
        usuarios = users[:max]
        thumbnail_options = dict(size=(20, 20), crop=True, bw=True)
    else:
        usuarios = users
        xy = tam / int((len(users) ** 0.5)+0.8)
        thumbnail_options = dict(size=(xy, xy), crop=True)
    for user in usuarios:
        retorno = ''
        tumb = get_thumbnailer(user.profileimage.image).get_thumbnail(thumbnail_options)
        retorno += '<a href="%s"><img src="%s" title="%s"/></a>' % (reverse('profiles', kwargs={'username': user.username, }), tumb.url, user.first_name)
    return retorno