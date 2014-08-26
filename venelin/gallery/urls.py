from django.conf.urls import url

from .views import galleries, gallery


urlpatterns = [
    url(r'^$', galleries, name='index'),
    url(r'^(?P<slug>[\w\_\-]+)/$', gallery, name='gallery'),
]
