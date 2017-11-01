from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.shortcuts import render
from django.views.static import serve

from .sitemap import sitemaps

admin.autodiscover()

urlpatterns = [
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^\.ckeditor/', include('ckeditor_uploader.urls')),

    url(r'^blog/', include('venelin.blog.urls', namespace='blog')),
    url(r'^links/', include('venelin.links.urls', namespace='links')),
    url(r'^gallery/', include('venelin.gallery.urls', namespace='gallery')),
    url(r'^highlighter/', include('venelin.syntaxhighlighter.urls')),
    url(r'^search/', render, {'template_name': 'search.html'}),

    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}),
    url(r'^robots\.txt$', render, {'template_name': 'robots.txt', 'content_type': 'text/plain; charset=utf-8'}),
    url(r'^(?P<path>favicon\.ico)$', serve, {'document_root': settings.STATIC_ROOT}),

    url(r'^', include('django.contrib.staticfiles.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + [

    url(r'^', include('venelin.pages.urls')),

]

if 'django_uwsgi' in settings.INSTALLED_APPS:
    urlpatterns.insert(0, url(r'^admin/uwsgi/', include('django_uwsgi.urls')))

if 'debug_toolbar' in settings.INSTALLED_APPS:
    import debug_toolbar
    urlpatterns.insert(0, url(r'^__debug__/', include(debug_toolbar.urls)))
