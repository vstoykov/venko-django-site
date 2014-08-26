from django.conf.urls import url

from .views import links

urlpatterns = [
    url(r'^$', links, name='index'),
]
