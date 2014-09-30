from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from django.db.models import signals, get_models
from django.utils.encoding import smart_unicode
from django.conf import settings


def update_contenttypes(app, **kwargs):
    #No post_syncdb o app e um object, ja no post_migrate e uma string
    if not isinstance(app, str):
        app = app.__name__.split('.')[-2]

    for ct in ContentType.objects.filter(app_label=app):
        try:
            name = smart_unicode(ct.model_class()._meta.verbose_name_raw)
            if ct.name != name:
                try: print u"Updating ContentType's name: '%s' -> '%s'" % (ct.name, name, )
                except: print u"Updating ContentType's ..."
                ct.name=name
                ct.save()
        except: pass


def update_permissions(app, **kwargs):
    #No post_syncdb o app e um object, ja no post_migrate e uma string
    if not isinstance(app, str):
        app = app.__name__.split('.')[-2]

    for ct in ContentType.objects.filter(app_label=app):
        for action in ('add', 'change', 'delete'):
            codename = u'%s_%s' % (action, ct.model)
            for permission in Permission.objects.filter(codename=codename):
                name = u'Can %s %s' % (action, ct.name)
                if permission.name != name:
                    try: print u"Updating Permission's name: '%s' -> '%s'" % (permission.name, name, )
                    except: print u"Updating Permission's ..."
                    permission.name=name
                    permission.save()


# Se tiver a aplicacao south no INSTALLED_APPS,
# ele conecta o update_contenttypes ao post_migrate
if 'south' in settings.INSTALLED_APPS:
    from south.signals import post_migrate
    post_migrate.connect(update_contenttypes)
    post_migrate.connect(update_permissions)

signals.post_syncdb.connect(update_contenttypes)
signals.post_syncdb.connect(update_permissions)