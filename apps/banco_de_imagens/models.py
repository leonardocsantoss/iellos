#-*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.db.models import signals
from django.template.defaultfilters import slugify
from tagging_autocomplete.models import TagAutocompleteField
from datetime import datetime
import settings


class Imagem(models.Model):
    
    criador = models.ForeignKey(User, related_name='imagem', verbose_name=_(u"Criador"))
    image = models.ImageField(upload_to=settings.BANCO_IMAGE_UPLOAD_DIR, verbose_name=_(u"Imagem"))
    slug = models.SlugField(max_length=65, unique=True, blank=True, verbose_name=_(u"Slug"))
    nome = models.CharField(max_length=60, verbose_name=_(u"Titulo"))
    desc = models.TextField(verbose_name=_(u"Descrição"))
    tags = TagAutocompleteField(verbose_name=_(u"Tags"))
    data_criacao = models.DateTimeField(default=datetime.now, verbose_name=_(u"Data de Criação"))

    def pontos(self):
        return Ponto.objects.filter(imagem=self)
    
    def __unicode__(self):
        return self.nome

    def get_absolute_url(self):
        return reverse('bi_imagem', kwargs={'slug': self.slug})

# SIGNAL, SEMPRE SALVAR O NOME DO ELO COMO SLUG.
def imagem_post_save(sender, instance, created, **kwargs):
    if created:
        instance.slug = u"%s-%s" % (instance.id, slugify(instance.nome))
        instance.save()
signals.post_save.connect(imagem_post_save, sender=Imagem)


class Ponto(models.Model):

    imagem = models.ForeignKey(Imagem, verbose_name=_(u"Imagem"))
    label = models.CharField(max_length=100, verbose_name=_(u"Titulo"))
    width = models.PositiveIntegerField(verbose_name=_(u"Largura"))
    height = models.PositiveIntegerField(verbose_name=_(u"Altura"))
    top = models.PositiveIntegerField(verbose_name=_(u"Cima"))
    left = models.PositiveIntegerField(verbose_name=_(u"Direita"))

    def __unicode__(self):
        return self.label