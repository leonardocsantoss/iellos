from django import forms
from models import Elo

class EloForm(forms.ModelForm):
    class Meta:
        model = Elo
        exclude = ('criador','data_criacao','membros','slug',)
        fields = ('nome', 'tipo', 'desc', )