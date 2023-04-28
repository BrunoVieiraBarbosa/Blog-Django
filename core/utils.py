from django.core.paginator import Paginator
from .models import Tag

def get_page(page_number):
    try:
        page_number = int(page_number)
        return 1 if page_number <= 0 else page_number
    except Exception:
        return 1


#Faz a paginação do blog, tanto para a home, new ou pesquisas
def paginate(paginator: Paginator, page):
    return paginator.page(1) if (page <= 0) else paginator.page(paginator.num_pages) if (page > paginator.num_pages) else paginator.page(page)


#Função auxiliar get retorna os posts de determinadas tags
def get_tags(tag_text: str):
    all_tags_posts = set(tag_text.split('-'))
    all_posts = []
    for tag in all_tags_posts:
        for i in Tag.objects.filter(name__icontains=tag):
            [all_posts.append(y) for y in i.post_set.all()]
    

    all_posts = {x: all_posts.count(x) for x in set(all_posts)}
    all_posts = sorted(all_posts, key=lambda x: all_posts[x], reverse=True)
    return all_posts, all_tags_posts