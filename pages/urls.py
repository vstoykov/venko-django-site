from django.conf.urls import url, patterns

urlpatterns = patterns('pages.views',
    url(r'^(?P<url>.+)', 'flatpage'),
    url(r'^$', 'flatpage', kwargs={'url': '/'}, name='home'),
)
