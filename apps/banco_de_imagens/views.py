# -*- coding:utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.paginator import Paginator, InvalidPage
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
from django.db.models import Q
from models import Imagem, Ponto
from forms import ImagemForm



@login_required
def index(request, template_name='banco_de_imagens/index.html'):
    
    imagens_list = Imagem.objects.all()
    if request.GET.get('tag'):
        imagens_list = imagens_list.filter(tags__contains=request.GET.get('tag'))
    if request.GET.get('q'):
        imagens_list = imagens_list.filter(Q(nome__contains=request.GET.get('q')) | Q(desc__contains=request.GET.get('q')))

    paginator = Paginator(imagens_list, 18)
    imagens = paginator.page(1)
    return render_to_response(template_name, {
        'imagens': imagens,
        'q': request.GET.get('q'),
        'tag': request.GET.get('tag'),
    },context_instance=RequestContext(request))


@login_required
def index_scroll(request, page, template_name='banco_de_imagens/imagens_scroll.html'):

    imagens_list = Imagem.objects.all()
    if request.GET.get('tag'):
        imagens_list = imagens_list.filter(tags__contains=request.GET.get('tag'))
    if request.GET.get('q'):
        imagens_list = imagens_list.filter(Q(nome__contains=request.GET.get('q')) | Q(desc__contains=request.GET.get('q')))

    paginator = Paginator(imagens_list, 18)
    try:
        imagens = paginator.page(page)
    except InvalidPage:
        raise Http404()
    return render_to_response(template_name, {
       'imagens': imagens
    },context_instance=RequestContext(request))



@login_required
def imagem(request, slug, template_name='banco_de_imagens/imagem.html'):
    imagem = get_object_or_404(Imagem, slug=slug)
    return render_to_response(template_name, {
        'imagem': imagem,
    },context_instance=RequestContext(request))


@login_required
def imagem_excluir(request, slug):
    imagem = get_object_or_404(Imagem, slug=slug, criador=request.user)
    imagem.delete()
    return HttpResponseRedirect(reverse('bi_index'))


@csrf_exempt
@login_required
def imagem_tags(request, slug):
    imagem = get_object_or_404(Imagem, slug=slug, criador=request.user)
    if request.method == 'POST':
        if request.POST.get('action') == 'delete':
            ponto = get_object_or_404(Ponto, id=request.POST.get('id'), imagem=imagem)
            ponto.delete()
        elif request.POST.get('action') == 'save':
            Ponto.objects.create(imagem=imagem, width=request.POST.get('width'), height=request.POST.get('height'), top=request.POST.get('top'), left=request.POST.get('left'), label=request.POST.get('label'))
    return HttpResponse('OK')


@login_required
def imagem_editar(request, slug, form_class=ImagemForm, template_name='banco_de_imagens/adicionar.html'):
    imagem = get_object_or_404(Imagem, slug=slug, criador=request.user)
    form = form_class(instance=imagem)
    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=imagem)
        if form.is_valid():
            imagem = form.save()
            return HttpResponseRedirect(imagem.get_absolute_url())
    return render_to_response(template_name, {
    'form': form,
    },context_instance=RequestContext(request))


@login_required
def adicionar(request, form_class=ImagemForm, template_name='banco_de_imagens/adicionar.html'):
    form = form_class()
    if request.method == 'POST':
        form = form_class(request.POST, request.FILES)
        if form.is_valid():
            form.instance.criador = request.user
            imagem = form.save()
            return HttpResponseRedirect(imagem.get_absolute_url())
    return render_to_response(template_name, {
    'form': form,
    },context_instance=RequestContext(request))

