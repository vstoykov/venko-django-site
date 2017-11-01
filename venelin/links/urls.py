from django.conf.urls import url

from .views import links

app_name = 'links'
urlpatterns = [
    url(r'^$', links, name='index'),
]
