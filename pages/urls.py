from django.conf.urls import url, patterns, include

urlpatterns = patterns('django.contrib.flatpages.views',
    url(r'^', include('django.contrib.flatpages.urls')),
    url(r'^$', 'flatpage', kwargs={'url': '/'}, name='home'),
)
