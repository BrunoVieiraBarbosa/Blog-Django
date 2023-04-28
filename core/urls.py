from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name='core'
urlpatterns = [
    path('', views.index, name='index'),

    path('new/', views.new, name='new-index'),

    path('politica/', views.politica, name='politica'),
    path('robots.txt', views.robots_text, name='robots'),

    path('post/<slug:slug>/', views.post, name='post_page'),

    path('search/', views.search_index, name='search'),

    path('tags/', views.tag_index, name='tag-index'),
    path('tags/name/<str:tag_text>/', views.tag_by_name, name='tag-name'),

    path('tags/search/', views.tag_by_search, name='tag-search'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
