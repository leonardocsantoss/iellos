# -*- coding:utf-8 -*-
from PIL import Image
from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from utils.widgets import MyDateWidget

try:
    import cStringIO as StringIO
except ImportError:
    import StringIO

from models import ProfileDefault



class ProfileImageForm(forms.Form):

    image = forms.FileField(label=_(u"Nova foto"))

    def clean_image(self):
        if 'image' in self.cleaned_data:
            image = self.cleaned_data['image']
            extensao = image.name.split('.')[-1].lower()
            if not extensao in ('png', 'jpg', 'gif'):
                raise forms.ValidationError(_(u'O arquivo que você está carregando não parece ser uma imagem.'))
            if image.size > settings.PROFILE_IMAGE_MAX_SIZE * 1024:
                raise forms.ValidationError(_(u'Certifique que o tamanho da imagem não utrapasse %d Kb.' % settings.PROFILE_IMAGE_MAX_SIZE))
            try:
                data = Image.open(StringIO.StringIO(image.read()))
                data.verify()
            except:
                raise forms.ValidationError(_(u'O arquivo que você está carregando não parece ser uma imagem.'))
            return image



class ProfileDefaultForm(forms.ModelForm):
    
    class Meta:
        model = ProfileDefault
        exclude = ('user', )
        fields = ('first_name', 'last_name', 'identidade_sexual', 'data_de_nascimento', 'relacionamento', 'cidade_natal', 'eu_sou', )
        widgets = {
            'data_de_nascimento': MyDateWidget(attrs={'style': 'width: 100px;'}),
        }

    first_name = forms.CharField(max_length=60, label=_(u'Nome'))
    last_name = forms.CharField(max_length=60, label=_(u'Sobrenome'))

    def __init__(self, *args, **kwargs):
        super(ProfileDefaultForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name

    def save(self, commit=True):
        instance = super(ProfileDefaultForm, self).save(commit=commit)
        instance.user.first_name = self.cleaned_data['first_name']
        instance.user.last_name = self.cleaned_data['last_name']
        instance.user.save()
