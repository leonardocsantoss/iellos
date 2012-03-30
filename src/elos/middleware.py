# -*- coding:utf-8 -*-
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext
from models import ConviteElo, VotacaoEloFechado


class Messages(object):
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.user.is_authenticated() and request.META.get('HTTP_REFERER') is not None and request.path in request.META.get('HTTP_REFERER'):
            for convite in ConviteElo.objects.filter(convidados=request.user):
                message=ugettext(u"<b>@%s</b> você foi convidado para conectar-se ao elo <a href=\"%s\">%s</a>. Você aceita?<br/><a href=\"%s?resp=nao\" style=\"float:right\">Não</a><a href=\"%s?resp=sim\" style=\"float:left\">Sim</a><br/>") % (request.user.username, convite.elo.get_absolute_url(), convite.elo.nome, reverse('conectar_elo', kwargs={'slug': convite.elo.slug }), reverse('conectar_elo', kwargs={'slug': convite.elo.slug }))
                if not request.user.message_set.filter(message=message).count():
                    request.user.message_set.create(message=message)
            for vot in VotacaoEloFechado.objects.filter(elo__membros=request.user).exclude(ja_votou=request.user):
                message=ugettext(u"<b>%s</b> você aceita <a href=\"%s\">@%s</a> conectar-se ao elo <a href=\"%s\">%s</a>?<br/><a href=\"javascript:none\" onClick=\"J.get('%s?voto=nao');if(J('.msgGrowl-content > ul > li').length > 1){J(this).parent().parent().remove();}else{J('#msgGrowl-container').fadeOut();}\" style=\"float:right\">Não</a><a href=\"javascript:none\" onClick=\"J.get('%s?voto=sim');if(J('.msgGrowl-content ul li').length > 1){J(this).parent().parent().remove();}else{J('#msgGrowl-container').fadeOut();}\" style=\"float:left\">Sim</a><br/>") % (request.user.username, reverse('profiles' ,kwargs={'username': vot.votado.username, }), vot.votado.username, vot.elo.get_absolute_url(), vot.elo.nome, reverse('votar_elo', kwargs={'username': vot.votado.username, 'slug': vot.elo.slug }), reverse('votar_elo', kwargs={'username': vot.votado.username, 'slug': vot.elo.slug }))
                if not request.user.message_set.filter(message=message).count():
                    request.user.message_set.create(message=message)