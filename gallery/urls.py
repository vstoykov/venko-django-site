from django.conf.urls.defaults import *

urlpatterns = patterns('gallery.views',
    url(r'^gallery/$', 'view_galleries', name='galleries'),
    url(r'^gallery/(?P<gallery>[\w\_\-]+)/$', 'view_galleries', name='gallery'),
)