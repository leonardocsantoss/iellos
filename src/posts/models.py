# -*- coding:utf-8 -*-
from datetime import datetime
import re

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.comments.models import Comment
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import signals
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from elos.models import Elo


#O unico ponto a ser questionado, é quando ao inicio do link, acredito eu que ele pode ser qualquer um menos " e '
#Pois se for " ou ' ele já será um link de uma imagem ou de um video

def imagem(text, link, link_url):
    return text.replace(force_unicode(link),u'<br/><img style="max-width:540px" src="%s"><br/>' % force_unicode(link_url))


def picasaAlbum(text, link, rex2):
    return text.replace(force_unicode(link),
        u"""
        <script type="text/javascript">
            var J = jQuery.noConflict();
            J(document).ready(function() {

            J("#album_%s").EmbedPicasaGallery('%s',{
                album: "%s",
                size: 64,
                rel: "%s",
                loading_animation: "%sielos/images/loading-image.gif",
                msg_more: 'Mais...',
                authkey: '%s',
                show_more: 6
            });

            });
        </script>
        <div id="album_%s"></div>""" % (datetime.now().strftime("%d_%m_%Y_%H_%M_%S"), force_unicode(rex2.group('id_user')), force_unicode(rex2.group('album')), datetime.now().strftime("%d_%m_%Y_%H_%M_%S"), settings.MEDIA_URL, force_unicode(rex2.group('authkey')), datetime.now().strftime("%d_%m_%Y_%H_%M_%S")))


def youtube(text, grupo, link):
    return text.replace(force_unicode(link), u'<iframe width="420" height="315" src="http://www.youtube.com/embed/%s?wmode=transparent" frameborder="0" allowfullscreen></iframe>' % grupo)

def vimeo(text, grupo, link):
    return text.replace(force_unicode(link), u'<iframe src="http://player.vimeo.com/video/%s" width="420" height="315" frameborder="0" webkitAllowFullScreen allowFullScreen></iframe>' % force_unicode(grupo))


def profile(text):
    retorno = text
    rex = re.compile(r'@\w+')
    for link in rex.findall(retorno):
        try:    
            usuario = User.objects.get(username=str(link).split('@')[1])
            retorno = retorno.replace(force_unicode(link), u"<a href=\"%s\">@%s</a>" % ( reverse('profiles', kwargs={'username': usuario.username, }), usuario.username) )
        except:
            pass
    return retorno


def url(text, link, link_url):
    if u'iellos.com/apps/' in link_url: classe = 'apps'
    else: classe = 'url'
    return text.replace(force_unicode(link), u'<a href="%s" target="_blank" class="%s" >%s</a>' % (force_unicode(link), classe, force_unicode(link_url)))


def parser(texto):
    retorno = texto

    #Expressões
    img_rex = re.compile(r'(?:(?P<http>https?://)|(?P<www>www.))(www.)?(\S+)(?:(?P<jpg>\.jpg)|(?P<png>\.png)|(?P<gif>\.gif))')
    picasa_rex = re.compile(r'(https?://)?(www.)?(picasaweb\.google\.com/)(?P<id_user>\d+)(/)(?P<album>\w+)(\?authkey=)?(?P<authkey>\w+)?')
    youtube_rex = re.compile(r'(https?://)?(www.)?(youtube\.com/watch\?)(\S*)(v=[0-9a-zA-Z]+)(\S*)')
    vimeo_rex = re.compile(r'(https?://)?(www.)?(vimeo\.com/)(\d+)')


    rex = re.compile(r'(?:(?P<http>https?://)|(?P<www>www.))(www.)?(\S+)')

    for grupos in rex.findall(retorno):
        link = u''.join(grupos)
        if not u'http://' in str(link) and not u'https://' in link:
            link_url = 'http://' + link
        else:
            link_url = link

        if(img_rex.findall(link)):
            retorno = imagem(retorno, link, link_url)

        elif (youtube_rex.findall(link)):
            retorno = youtube(retorno, youtube_rex.findall(link)[0][-2].replace('v=', ''), link)

        elif(picasa_rex.findall(link)):
            retorno = picasaAlbum(text, link, picasa_rex.search(link))

        elif (vimeo_rex.findall(link)):
            retorno = vimeo(retorno,vimeo_rex.findall(link)[0][-1],link)
            
        else:
            retorno = url(retorno, link, link_url)

    retorno = profile(retorno)
    return retorno


def escape(texto):
    texto = mark_safe(force_unicode(texto).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;'))
    texto = texto.replace('&lt;b&gt;', '<b>').replace('&lt;/b&gt;', '</b>').replace('&lt;i&gt;', '<i>').replace('&lt;/i&gt;', '</i>').replace('&lt;s&gt;', '<s>').replace('&lt;/s&gt;', '</s>').replace('&lt;u&gt;', '<u>').replace('&lt;/u&gt;', '</u>')
    texto = texto.replace('\n', '<br/>')
    return texto

class Post(models.Model):

    elos = models.ManyToManyField(Elo, blank=True)
    user = models.ForeignKey(User)
    data_de_criacao = models.DateTimeField(default=datetime.now)
    data_de_atualizacao = models.DateTimeField(default=datetime.now)
    texto = models.TextField()

    def __unicode__(self):
        return u'Post de %s, em %s' % (self.user, self.data_de_criacao)

#Motor parser do Post
def motor_parser(sender, instance, created, **kwargs):
    if created:
        instance.texto = parser(escape(instance.texto))
        instance.save()
signals.post_save.connect(motor_parser, sender=Post)

#Motor parser do Comentário
def motor_parser_comment(sender, instance, created, **kwargs):
    if created:
        instance.comment = parser(escape(instance.comment))
        instance.save()
signals.post_save.connect(motor_parser_comment, sender=Comment)

#Atualização da data_de_atualização do post quando há um comentário
def update_date_post_comment(sender, instance, created, **kwargs):
    try:
        post = Post.objects.get(id=instance.object_pk)
        post.data_de_atualizacao=instance.submit_date
        post.save()
    except:
        pass
signals.post_save.connect(update_date_post_comment, sender=Comment)