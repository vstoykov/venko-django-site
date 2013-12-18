from django.conf.urls import url, patterns

urlpatterns = patterns('gallery.views',
    url(r'^$', 'galleries', name='index'),
    url(r'^(?P<slug>[\w\_\-]+)/$', 'gallery', name='gallery'),
)
