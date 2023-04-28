from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

admin.site.site_header = 'Blog'
admin.site.site_title = 'Blog'
admin.site.index_title = 'Administração'

handler404 = 'core.views.handler404'


urlpatterns = [
    path('', include('core.urls')),
    path('api/', include('api.urls')),
    path('admin/', admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)