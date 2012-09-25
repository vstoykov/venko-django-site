from django.conf.urls.defaults import *

urlpatterns = patterns('django.contrib.flatpages.views',
	url(r'^$', 'flatpage', kwargs={'url': '/'}, name='home'),
) + patterns('django.views.generic.simple',
    #url(r'^$', 'direct_to_template', kwargs={'template': 'home.html'}, name='home'),

    # Old Gallery URL
    url(r'^gallery_static/$', 'direct_to_template', {'template': 'gallery_static.html'}),
)
