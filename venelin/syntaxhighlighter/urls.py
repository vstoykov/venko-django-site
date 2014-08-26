from django.conf.urls import url

from .views import highlight

urlpatterns = [
    url(r'^$', highlight, name='highlighter'),
]
