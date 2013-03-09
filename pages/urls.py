from django.conf.urls import url, patterns

urlpatterns = patterns('django.contrib.flatpages.views',
    url(r'^$', 'flatpage', kwargs={'url': '/'}, name='home'),
)
