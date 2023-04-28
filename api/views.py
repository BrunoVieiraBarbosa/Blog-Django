from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from core.models import Post, Tag

# Create your views here.

def get_post(request: WSGIRequest, id: int):
    post_ = list(Post.objects.filter(id=id))
    if (post_ != []):
        post_ = post_[0]
        response_data = {
        "title": post_.title,
        "description": post_.description,
        "text": post_.text,
        "tags": [{"name": tag.name, "category": tag.category.all()[0].name} for tag in post_.tags.all()],
        "thumb": post_.thumb.url,
        "pub_date": post_.pub_date.strftime("%d/%m/%Y"),
        "previous_post": post_.previous_post.all()[0].id if len(post_.previous_post.all())>0 else None,
        "next_post": post_.next_post.all()[0].id if len(post_.next_post.all())>0 else None
        }
        return JsonResponse(response_data)
    else:
        return JsonResponse({})


def search(request: WSGIRequest, text: str):
    response = {}
    if text == "":
        return JsonResponse({})

    if text.lower().startswith('tag:'):
        text_search = text[4:].split(' ')
        response = {'data': [f"tag:{i.name}" for tag in text_search for i in Tag.objects.filter(name__icontains=tag)][:5]}
    else:
        response = {'data': [post_.title for post_ in Post.objects.filter(title__icontains=text)][:5]}
    return JsonResponse(response)