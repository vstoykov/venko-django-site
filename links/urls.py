from django.conf.urls.defaults import *

urlpatterns = patterns('links.views',
    url(r'^$', 'links', name='links'),
)