from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.shortcuts import render
from django.views.static import serve

from .sitemap import sitemaps
from .api import whoami

admin.autodiscover()

urlpatterns = [
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
    path('auth/', include('social_django.urls', namespace='social')),

    path('blog/', include('venelin.blog.urls', namespace='blog')),
    path('links/', include('venelin.links.urls', namespace='links')),
    path('gallery/', include('venelin.gallery.urls', namespace='gallery')),
    path('highlighter/', include('venelin.syntaxhighlighter.urls')),
    path('search/', render, {'template_name': 'search.html'}),

    path('api/whoami', whoami),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),
    path('robots.txt', render, {'template_name': 'robots.txt', 'content_type': 'text/plain; charset=utf-8'}),
    path('favicon.ico', serve, {'document_root': settings.STATIC_ROOT, 'path': 'favicon.ico'}),

    path('', include('django.contrib.staticfiles.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + [

    path('', include('venelin.pages.urls')),
]

if 'django_uwsgi' in settings.INSTALLED_APPS:
    urlpatterns.insert(0, path('admin/uwsgi/', include('django_uwsgi.urls')))

if 'debug_toolbar' in settings.INSTALLED_APPS:
    import debug_toolbar
    urlpatterns.insert(0, path('__debug__/', include(debug_toolbar.urls)))
