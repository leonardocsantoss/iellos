# -*- coding:utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.views.generic.simple import direct_to_template
from django.conf import settings
from forms import ProfileImageForm, ProfileDefaultForm
from django.utils.translation import ugettext_lazy as _, ugettext
from models import ProfileImage, ProfileDefault
from django.shortcuts import get_object_or_404
import os
from django.db.models import Q

from posts.models import Post
from elos.models import Elo


@login_required
def upload_profile_image(request):
    form = ProfileImageForm()
    if request.method == 'POST':
        profile = ProfileImage.objects.get_or_create(user=request.user)
        form = ProfileImageForm(request.POST, request.FILES)
        if form.is_valid():
            extensao = request.FILES['image'].name.split('.')[-1].lower()
            filename = u"%s/%s%s.%s" % (settings.MEDIA_ROOT, settings.PROFILE_IMAGE_UPLOAD_DIR, request.user.id, extensao)
            try:
                os.unlink(profile[0].image.path)
            except:
                pass
            profile[0].image.save(filename, request.FILES['image'])
            request.user.message_set.create(message=ugettext(u"<b>@%s</b> sua foto foi alterada com sucesso!") % request.user.username)
    return direct_to_template(request, 'profiles/image_upload.html', {'image_upload_form': form})


def profiles(request, username):
    profile_default = get_object_or_404(ProfileDefault, user__username=username)
    return direct_to_template(request, 'profiles/profiles.html', {'profile_default': profile_default})


@login_required
def edit_profile_default(request):
    profile = ProfileDefault.objects.get_or_create(user=request.user)[0]
    form = ProfileDefaultForm(instance=profile)
    if request.method == 'POST':
        form = ProfileDefaultForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            request.user.message_set.create(message=ugettext(u"<b>@%s</b> seu perfil foi alterado com sucesso!") % request.user.username )
    return direct_to_template(request, 'profiles/edit_default_profile.html', {'form': form})



@login_required
def pesquisa(request):
    q = request.GET.get('q', '')
    result_profs = ProfileDefault.objects.filter(Q(eu_sou__icontains=q) | Q(user__first_name__icontains=q) | Q(user__last_name__icontains=q) | Q(identidade_sexual__icontains=q) | Q(relacionamento__icontains=q) | Q(cidade_natal__icontains=q)).distinct()
    result_elos = Elo.objects.filter(Q(nome__icontains=q) | Q(desc__icontains=q) | Q(membros__first_name__icontains=q) | Q(membros__last_name__icontains=q)).distinct()
    result_posts = Post.objects.filter(Q(texto__icontains=q) | Q(user__first_name__icontains=q) | Q(user__last_name__icontains=q) | Q(elos__nome__icontains=q) | Q(elos__desc__icontains=q)).exclude(Q(elos__tipo='F') & ~Q(elos__membros=request.user)).distinct()
    return direct_to_template(request, 'profiles/pesquisa.html', {'result_profs': result_profs, 'result_elos': result_elos, 'result_posts': result_posts, 'q': q})


def select_app(request, app):
    return direct_to_template(request, 'profiles/select_app.html', {'app': app})


def add_app(request):
    if request.method == 'POST':
        if request.POST.get('app'):
            request.user.profiledefault.add_app(request.POST.get('app'))
    myapps = request.user.profiledefault.apps_list()
    apps = [app for app in settings.APPS_LIST if app not in myapps]
    return direct_to_template(request, 'profiles/add_app.html', {'apps': apps})