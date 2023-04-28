from django.urls import path
from . import views


app_name='api'
urlpatterns = [
    # path('post/<int:id>', views.get_post),
    path('search/<str:text>', views.search, name='search'),
]