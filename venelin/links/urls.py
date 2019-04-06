from django.urls import path

from .views import links

app_name = 'links'
urlpatterns = [
    path('', links, name='index'),
]
