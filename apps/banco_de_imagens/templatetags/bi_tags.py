# -*- coding:utf-8 -*-
from django import template
from django.core.urlresolvers import reverse
from tagging.models import Tag

register = template.Library()


@register.simple_tag
def tags_menu():
    tags = Tag.objects.all()
    retorno = u''
    for tag in tags:
        retorno += u'<li><a href="%s?tag=%s" class="ui-nav-item">%s</a></li>' % (reverse('bi_index'), tag, tag)
    return retorno