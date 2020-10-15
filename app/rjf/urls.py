from django.conf import settings
from django.urls import path, include
from django.contrib import admin

from core import urls as core_urls


urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('', include(core_urls)),
]


if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
