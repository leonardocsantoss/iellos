# -*- coding:utf-8 -*-
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models import signals
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

try:
    import cStringIO as StringIO
except ImportError:
    import StringIO

try:
    import hashlib.md5 as md5
except ImportError:
    import md5 as md5

import httplib



class ProfileImage(models.Model):

    class Meta:
        verbose_name = _(u'Imagem do profile')
        verbose_name_plural = _(u'Imagens dos profiles')

    user = models.OneToOneField(User, unique=True)
    image = models.ImageField(upload_to=settings.PROFILE_IMAGE_UPLOAD_DIR, null=True)

    def __unicode__(self):
        return u'Foto de %s' % self.user

def create_default_profile_image(sender, created, instance, **kwargs):
    profile, prof_created = ProfileImage.objects.get_or_create(user=instance)
    if prof_created:
        conn = httplib.HTTPConnection("www.gravatar.com")
        conn.request("GET", "/avatar/%s?s=256" % md5.md5(profile.user.email.lower()).hexdigest(), None, {"Accept": "image/gif"})
        r = conn.getresponse()
        data = r.read()
        filename = '%s%s.%s' % (settings.PROFILE_IMAGE_UPLOAD_DIR, instance.id, 'png')
        arq = open('%s/%s' %(settings.MEDIA_ROOT, filename),"wb")
        arq.write(data)
        arq.close()
        conn.close()
        profile.image = filename
        profile.save()
signals.post_save.connect(create_default_profile_image, sender=User)




class Profile(models.Model):

    class Meta:
        abstract = True

    user = models.OneToOneField(User, unique=True)

    def get_absolute_url(self):
        return reverse('profiles', kwargs={'username': self.user.username})

    def __unicode__(self):
        return u'Perfil de %s' % self.user



class ProfileDefault(Profile):

    SEXO_CHICES = (
        ('', _(u'Prefiro não informar')),
        ('MASCULINO', _(u'Masculino')),
        ('FEMININO', _(u'Feminino')),
    )
    RELACIONAMENTO_CHICES = (
        ('', _(u'Prefiro não informar')),
        ('SOLTEIRO', _(u'Solteiro')),
        ('NAMORANDO', _(u'Namorando')),
        ('NOIVO', _(u'Noivo')),
        ('ENROLADO', _(u'Enrolado')),
        ('EM_BUSCA', _(u'Em busca')),
        ('CASADO', _(u'Casado')),
        ('VIUVO', _(u'Viuvo')),
        ('DIVORCIADO', _(u'Divorciado')),
        ('SEPARADO', _(u'Separado')),
    )

    class Meta:
        verbose_name = _(u'Profile padrão')
        verbose_name_plural = _(u'Profiles padrão')

    eu_sou = models.TextField(default=_(u"Um breve texto sobre mim!"))
    identidade_sexual = models.CharField(blank=True, null=True, max_length=9, choices=SEXO_CHICES, verbose_name=_(u"Identidade sexual"))
    data_de_nascimento = models.DateField(blank=True, null=True, verbose_name=_(u"Data de nascimento"))
    relacionamento = models.CharField(blank=True, null=True, max_length=10, choices=RELACIONAMENTO_CHICES, verbose_name=_(u"Relacionamento"))
    cidade_natal = models.CharField(blank=True, null=True, max_length=60, verbose_name=_(u"Cidade natal"))
    apps = models.TextField(blank=True, null=True, max_length=255)

    def add_app(self, app):
        if app in settings.APPS_LIST and not app in self.apps_list():
            if self.apps:
                self.apps = self.apps+" %s" % app
            else:
                self.apps = app
            self.save()
            return True
        return False
        
    def apps_list(self):
        if self.apps:
            return self.apps.split(' ')
        else:
            return list()



def create_default_profile(sender, created, instance, **kwargs):
    ProfileDefault.objects.get_or_create(user=instance)
signals.post_save.connect(create_default_profile, sender=User)
