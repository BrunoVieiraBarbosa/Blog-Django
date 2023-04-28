from django.core.handlers.wsgi import WSGIRequest
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse
from .models import Post, Category, LandingPage
from .utils import get_tags, paginate, get_page


#Trata sobre paginas não existentes
def handler404(request: WSGIRequest, exception):
    return render(request, 'posts/Not Found.html', {'erro': "Essa pagina não existe"})


#Trata das requisição para a pagina principal
def index(request: WSGIRequest):
    posts_ = Post.objects.all().order_by('-pub_date')[:3]
    try:
        projects = LandingPage.objects.get(id='1')
    except Exception:
        projects = None

    response = render(request, "posts/landing.html", context={'last_posts': posts_, 'projects': projects})
    return response


#Trata das requisição para a pagina New
def new(request: WSGIRequest):
    paginator_ = Paginator(Post.objects.all().order_by('-pub_date'), 10)
    page_number = get_page(request.GET.get('page'))

    posts_ = paginate(paginator_, page_number)

    context = {'posts': posts_, 'title': "News", 'page':'new',
    'text_redirect': reverse('core:new-index'), 'num_pages': paginator_.num_pages,
    'description': 'Ultimos posts e projetos lançados'}
    return render(request, "posts/index.html", context=context)


#Trata das requisição para a pagina de post
def post(request: WSGIRequest, slug: str):
    post_ = get_object_or_404(Post, slug=slug)

    context = {
        'post': post_,
        'previous_post': list(post_.previous_post.all()),
        'next_post': list(post_.next_post.all()),
        'page':None
    }

    context['previous_post'] = None if context['previous_post'] == [] else context['previous_post'][0]
    context['next_post'] = None if context['next_post'] == [] else context['next_post'][0]

    all_posts = [y for x in post_.tags.all() for y in x.post_set.all()]

    all_posts = {x: all_posts.count(x) for x in set(all_posts)}
    all_posts = sorted(all_posts, key=lambda x: all_posts[x], reverse=True)

    try:
        all_posts.remove(post_)
    except Exception:
        pass

    context['suggestions'] = all_posts[:4] if all_posts != [] else None

    return render(request, "posts/post.html", context=context)


#Trata das requisição para a pagina de tags (Mostras as tags)
def tag_index(request: WSGIRequest):
    tags = {category.name: category.tag_set.all() for category in Category.objects.all()}
    return render(request, "posts/tags.html", context={'categories': tags, 'title': "Tags", 'page':'tags'})


#Trata das requisição por uma tag especifica e chama o paginador
def tag_by_name(request: WSGIRequest, tag_text: str):
    all_posts, all_tags_posts = get_tags(tag_text)
    page_number = get_page(request.GET.get('page'))

    if all_posts == []:
        return render(request, "posts/Not Found.html", {"erro": f"Not Found: {tag_text}"})

    title = "tag: " + ", ".join(all_tags_posts)

    paginator_ = Paginator(all_posts, 10)

    posts_ = paginate(paginator_, page_number)

    context = {'posts': posts_, 'title': title, 'page':'tags', 'num_pages': paginator_.num_pages,
            'text_redirect': reverse('core:tag-name', kwargs={'tag_text': tag_text}), 'search': True}
    return render(request, "posts/index.html", context=context)


#Trata das requisição da procura por uma tag e chama o paginador
def tag_by_search(request: WSGIRequest):
    search_text = request.GET.get('search').strip()
    page_number = get_page(request.GET.get('page'))

    all_posts, all_tags_posts = get_tags(search_text)
    if all_posts == []:
        return render(request, "posts/Not Found.html", {"erro": f"Not Found: {search_text}"})

    title = "tag: " + ", ".join(all_tags_posts)

    paginator_ = Paginator(all_posts, 10)

    posts_ = paginate(paginator_, page_number)

    context = {'posts': posts_, 'title': title, 'page':'tags', 'search_text': search_text,
                'num_pages': paginator_.num_pages, 'text_redirect': reverse('core:tag-search'), 'search': True}
    return render(request, "posts/index.html", context=context)


#Trata das requisição de pesquisar e chama o paginador caso seja uma pesquisa avulsa
def search_index(request: WSGIRequest):
    search_text = request.GET.get('search').strip()
    page_number = get_page(request.GET.get('page'))

    if (search_text == ''):
        return redirect("/new")

    if ((search_text != None) and search_text.startswith('tag:')):
        return redirect(f'/tags/search/?search={search_text[4:]}&page={page_number}')

    else:
        posts_ = Post.objects.filter(title__icontains=search_text).order_by('-pub_date')

        if list(posts_) == []:
            posts_ = Post.objects.filter(slug__icontains=search_text).order_by('-pub_date')
            if list(posts_) == []:
                return render(request, "posts/Not Found.html", {"erro": f"Not Found: {search_text}"})

        paginator_ = Paginator(posts_, 10)

        posts_ = paginate(paginator_, page_number)

        context = {'posts': posts_, 'title': f"search: {search_text}", 'search_text': search_text, 'page':'',
                    'num_pages': paginator_.num_pages, 'text_redirect': reverse('core:search'), 'search': True}
        return render(request, "posts/index.html", context=context)


#Retorna a politica de privacidade do site
def politica(request: WSGIRequest):
    context = {'title': "Politica de Privacidade"}
    return render(request, "politica/politica.html", context=context)


#Retorna um txt dos site permitidos e negados para robos
def robots_text(request: WSGIRequest):
    lines = [
            "User-Agent: *\n",
            "Disallow: /admin/",
        ]
    return HttpResponse("\n".join(lines), content_type="text/plain")
