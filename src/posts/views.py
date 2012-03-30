# -*- coding:utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.views.generic.simple import direct_to_template
from django.core.paginator import Paginator, InvalidPage
from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
from models import Post
from forms import PostForm
from elos.models import Elo
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.contrib.comments import Comment

@login_required
def user_posts(request):
    elos = Elo.objects.filter(membros=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST)
        form.fields['elos'].queryset = elos
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            if not len(form.instance.elos.all()):
                for elo in elos:
                    form.instance.elos.add(elo)
                
            form = PostForm()
            form.fields['elos'].queryset = elos
    else:
        form = PostForm(request.GET)
        form.fields['elos'].queryset = elos
    posts_list = Post.objects.filter(Q(user=request.user) | Q(elos__membros=request.user)).order_by('-data_de_atualizacao', '-data_de_criacao').distinct()
    paginator = Paginator(posts_list, 10)
    posts = paginator.page(1)
    return direct_to_template(request, 'posts/user_posts.html', {'posts': posts, 'form': form,})



@login_required
def delete_ajax(request,post_id):
    try:
        post = Post.objects.get(id=post_id)
        comments = Comment.objects.filter(object_pk=post_id)
        if post.user == request.user:
            post.delete()
            for c in comments:
                c.delete()
        return HttpResponse('OK')
    except:
        raise Http404()


@login_required
def delete_comment_ajax(request, comment_id):
    try:
        comment = Comment.objects.get(id=comment_id)
        if comment.user == request.user:
            comment.delete()
        return HttpResponseRedirect('%s?post_id=%s' % (reverse('user_posts_scroll', kwargs={'page': 1}), comment.object_pk))
    except:
        raise Http404()



@login_required
def user_posts_scroll(request, page):

    posts_list = Post.objects.filter(Q(user=request.user) | Q(elos__membros=request.user)).order_by('-data_de_atualizacao', '-data_de_criacao').distinct()

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            if not len(form.instance.elos.all()):
                for elo in  Elo.objects.filter(membros=request.user):
                    form.instance.elos.add(elo)
        else:
            raise Http404()
    else:
        post_id = request.GET.get('post_id')
        if post_id:
            posts_list = posts_list.filter(id=post_id)
    paginator = Paginator(posts_list, 10)
    try:
        posts = paginator.page(page)
    except InvalidPage:
        raise Http404()
    return direct_to_template(request, 'posts/user_posts_scroll.html', {'posts': posts, 'next' : reverse('posts.views.user_posts')})



def elo_posts_scroll(request, slug, page):
    try:
        elo = Elo.objects.filter(Q(tipo='A') | Q(membros=request.user.id)).filter(slug=slug)[0]
    except:
        raise Http404()

    posts_list = Post.objects.filter(elos=elo).order_by('-data_de_atualizacao', '-data_de_criacao')
    
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            form.instance.elos.add(elo)
        else:
            raise Http404()
    else:
        post_id = request.GET.get('post_id')
        if post_id:
            posts_list = posts_list.filter(id=post_id)

    paginator = Paginator(posts_list, 10)
    try:
        posts = paginator.page(int(page))
    except InvalidPage:
        raise Http404()
    return direct_to_template(request, 'posts/user_posts_scroll.html', {'posts': posts,})
