# -*- coding:utf-8 -*-
from django.http import HttpResponseRedirect, Http404, HttpResponse
from elos.forms import EloForm
from elos.models import Elo, VotacaoEloFechado, ConviteElo
from django.views.generic.simple import direct_to_template
from django.utils.translation import ugettext
from django.core.paginator import Paginator, InvalidPage
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from posts.models import Post
from posts.forms import PostForm
from profiles.models import ProfileDefault
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils.encoding import force_unicode



@login_required
def criar(request):
    if request.method == "POST":
        form_criar = EloForm(request.POST)
        if form_criar.is_valid():
            form_criar.instance.criador = request.user
            form_criar.instance.nome = force_unicode(form_criar.instance.nome).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;')
            form_criar.save()
            form_criar.instance.membros.add(request.user)
            request.user.message_set.create(message=ugettext(u"Elo !<a href=\"%s\">%s</a> foi criado com sucesso!") % (form_criar.instance.get_absolute_url(), form_criar.instance.nome ))
            return HttpResponseRedirect(form_criar.instance.get_absolute_url())
    else:
        form_criar = EloForm()
    return direct_to_template(request, 'elos/criar.html', {'form_criar': form_criar})



def elo(request, slug):
    elo = get_object_or_404(Elo, slug=slug)
    ctx = {'elo':elo, }
    if elo.tipo == 'A' or request.user in elo.membros.all():
        if request.user in elo.membros.all():
            if request.method == 'POST':
                form = PostForm(request.POST)
                if form.is_valid():
                    form.instance.user = request.user
                    form.save()
                    form.instance.elos.add(elo)
                    form = PostForm()
            else:
                form = PostForm(request.GET)
            ctx['form'] = form

        post_id = request.GET.get('post_id')
        if post_id:
            posts_list = Post.objects.filter(elos=elo, id=post_id).order_by('-data_de_atualizacao', '-data_de_criacao')
        else:
            posts_list = Post.objects.filter(elos=elo).order_by('-data_de_atualizacao', '-data_de_criacao')
        paginator = Paginator(posts_list, 10)
        posts = paginator.page(1)

        ctx['posts'] = posts
        return direct_to_template(request, 'elos/elo_posts.html', ctx)
    return HttpResponseRedirect(reverse('usuarios_elo', kwargs={'slug': slug}))



def usuarios_elo(request, slug):
    elo = get_object_or_404(Elo, slug=slug)
    return direct_to_template(request, 'elos/elo_usuario.html', {'elo':elo,})



@login_required
def convidar_user_elo(request, slug):
    elo = get_object_or_404(Elo, slug=slug)
    convite = ConviteElo.objects.get_or_create(elo=elo)[0]
    
    usuarios_list = ProfileDefault.objects.filter(~Q(user__in=elo.membros.all()) & ~Q(user__in=convite.convidados.all())).order_by('-user__last_login')

    if request.method == 'POST':
        username = request.POST.get('username')
        usuario = get_object_or_404(User, username=username)
        convite.convidados.add(usuario)
    else:
        q = request.GET.get('q')
        if q:
            usuarios_list = usuarios_list.filter(Q(user__first_name__icontains=q) | Q(user__last_name__icontains=q)).order_by('-user__last_login')

    paginator = Paginator(usuarios_list, 50)
    usuarios = paginator.page(1)
    return direct_to_template(request, 'elos/convidar.html', {'elo':elo, 'usuarios': usuarios, })


@login_required
def sair_elo(request, slug):
    elo = get_object_or_404(Elo, slug=slug, membros=request.user)
    elo.membros.remove(request.user)
    if not len(elo.membros.all()):
        elo.delete()
        request.user.message_set.create(message=ugettext(u"<b>@%s</b> você acaba de sair do elo <s>%s</s>!<br/>Com sua saída o elo deixou de existir!") % (request.user.username, elo.nome ))
    else:
        request.user.message_set.create(message=ugettext(u"<b>@%s</b> você acaba de sair do elo <a href=\"%s\">%s</a>!") % (request.user.username, elo.get_absolute_url(), elo.nome ))
    return HttpResponseRedirect('/')



@login_required
def conectar_elo(request, slug):
    elo = get_object_or_404(Elo, slug=slug)
    convite = ConviteElo.objects.get_or_create(elo=elo)[0]

    if elo.tipo == 'A':
        resp = request.GET.get('resp', 'sim')
        if resp == 'sim':
            elo.membros.add(request.user)
            convite.convidados.remove(request.user)
            request.user.message_set.create(message=ugettext(u"<b>@%s</b> você acaba de se conectar ao elo <a href=\"%s\">%s</a>!") % (request.user.username, elo.get_absolute_url(), elo.nome ))
        else:
            convite.convidados.remove(request.user)
            return HttpResponseRedirect('/')
    else:
        if request.user in convite.convidados.all():
            resp = request.GET.get('resp', 'nao')
            if resp == 'sim':
                elo.membros.add(request.user)
                convite.convidados.remove(request.user)
                request.user.message_set.create(message=ugettext(u"<b>@%s</b> você acaba de se conectar ao elo <a href=\"%s\">%s</a>!<br/>Já havia um convite para você participar desse elo!") % (request.user.username, elo.get_absolute_url(), elo.nome ))
            else:
                convite.convidados.remove(request.user)
                return HttpResponseRedirect('/')
        else:
            vot = VotacaoEloFechado.objects.get_or_create(elo=elo, votado=request.user)[0]
            request.user.message_set.create(message=ugettext(u"<b>@%s</b> seu pedido de conexão ao elo <a href=\"%s\">%s</a>, será votado pelos membros!") % (request.user.username, elo.get_absolute_url(), elo.nome ))
    return HttpResponseRedirect(elo.get_absolute_url())



@login_required
def votar_elo(request, username, slug):
    vot_elo = get_object_or_404(VotacaoEloFechado, elo__slug=slug, elo__membros=request.user, votado__username=username)
    if vot_elo.verifica():
        if not request.user in vot_elo.ja_votou.all():
            voto = request.GET.get('voto', 'nao')
            if voto == 'nao':
                vot_elo.nao = vot_elo.nao+1
            elif voto == 'sim':
                vot_elo.sim = vot_elo.sim+1
            vot_elo.ja_votou.add(request.user)
            vot_elo.save()
            vot_elo.verifica()

    return HttpResponse('OK')



def all_elos(request, page=1):
    elos_list = Elo.objects.all()
    paginator = Paginator(elos_list, 10)
    try:
        elos = paginator.page(int(page))
    except InvalidPage:
        raise Http404()
    if int(page) == 1:
        return direct_to_template(request, 'elos/all.html', {'elos': elos,})
    else:
        return direct_to_template(request, 'elos/scroll_all.html', {'elos': elos,})