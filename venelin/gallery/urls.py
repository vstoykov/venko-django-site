from django.conf.urls import url, patterns

from .views import galleries, gallery


urlpatterns = patterns('',
    url(r'^$', galleries, name='index'),
    url(r'^(?P<slug>[\w\_\-]+)/$', gallery, name='gallery'),
)
