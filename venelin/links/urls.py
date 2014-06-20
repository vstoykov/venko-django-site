from django.conf.urls import url, patterns

from .views import links

urlpatterns = patterns('links.views',
    url(r'^$', links, name='index'),
)
