from django.conf.urls import url, patterns

from .views import highlight

urlpatterns = patterns('',
    url(r'^$', highlight, name='highlighter'),
)
