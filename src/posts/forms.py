# -*- coding:utf-8 -*-
from django import forms
from models import Post

class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        exclude = ('user', 'data_de_criacao', 'data_de_atualizacao' )