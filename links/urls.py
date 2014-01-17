from django.conf.urls import url, patterns

urlpatterns = patterns('links.views',
    url(r'^$', 'links', name='index'),
)
