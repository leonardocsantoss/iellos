#-*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.db.models import signals
from django.template.defaultfilters import slugify
from datetime import datetime


class Elo(models.Model):
    TIPO_CHOICES = (
        ('A', _(u'Aberto')),
        ('F', _('Fechado')),
    )
    
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES, default="A", verbose_name=_(u"Tipo"))
    nome = models.CharField(max_length=30, unique=True, verbose_name=_(u"Nome do Elo"))
    desc = models.TextField(verbose_name=_(u"Descrição"))
    slug = models.SlugField(max_length=150, unique=True, blank=True, verbose_name=_(u"Slug"))
    criador = models.ForeignKey(User, related_name='criador',verbose_name=_(u"Criador"))
    data_criacao = models.DateTimeField(default=datetime.now, verbose_name=_(u"Data de Criação"))
    membros = models.ManyToManyField(User, symmetrical=False, related_name='membros', verbose_name=_(u"Membros"))

    def __unicode__(self):
        return self.nome

    def get_absolute_url(self):
        return reverse('elos.views.elo', kwargs={'slug': self.slug})

# SIGNAL, SEMPRE SALVAR O NOME DO ELO COMO SLUG.
def elo_slug_pre_save(signal, instance, sender, **kwargs):
    slug = slugify(instance.nome)
    new_slug = slug
    counter = 0
    while Elo.objects.filter(slug=new_slug).exclude(id=instance.id).count() > 0:
        counter += 1
        new_slug = '%s-%d'%(slug, counter)
    instance.slug = new_slug
signals.pre_save.connect(elo_slug_pre_save, sender=Elo)




class VotacaoEloFechado(models.Model):

    elo = models.ForeignKey(Elo, related_name='elo')
    votado = models.ForeignKey(User, related_name='user')
    sim = models.PositiveIntegerField(default=0)
    nao = models.PositiveIntegerField(default=0)
    ja_votou = models.ManyToManyField(User, blank=True, null=True, related_name='ja_votou')
    data_de_abertura = models.DateTimeField(default=datetime.now)

    def verifica(self):
        if len(self.elo.membros.all()) == len(self.ja_votou.all()):
            if self.sim >= self.nao:
                self.elo.membros.add(self.votado)
                self.votado.message_set.create(message=ugettext(u"<b>@%s</b> você acaba de ser aceito no elo <a href=\"%s\">%s</a>!") % (self.votado.username, self.elo.get_absolute_url(), self.elo.nome ))
                self.delete()
            else:
                self.votado.message_set.create(message=ugettext(u"<b>@%s</b> você não foi aceito no elo <a href=\"%s\">%s</a>!") % (self.votado.username, self.elo.get_absolute_url(), self.elo.nome ))
                self.delete()
            return False
        return True

    def __unicode__(self):
        return u"Votação %s/%s" % (self.votado, self.elo)



class ConviteElo(models.Model):

    elo = models.ForeignKey(Elo, related_name='convite_elo')
    convidados = models.ManyToManyField(User, blank=True, null=True, related_name='convidados')

    def __unicode__(self):
        return u"Convite %s/" % self.elo