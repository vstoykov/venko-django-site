from django.conf.urls import url, patterns

from .views import flatpage

urlpatterns = patterns('',
    url(r'^(?P<url>.+)', flatpage),
    url(r'^$', flatpage, kwargs={'url': '/'}, name='home'),
)
