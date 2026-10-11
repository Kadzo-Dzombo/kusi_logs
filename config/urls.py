from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

from .views import homepage


urlpatterns = [
    path('', homepage, name='homepage'),
    path('', include('yard.urls')),
    path('admin/', admin.site.urls),
]


if settings.DEBUG:
    if settings.DEBUG:
        urlpatterns += static(settings.STATIC_URL,
                              document_root=settings.STATIC_ROOT)
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)