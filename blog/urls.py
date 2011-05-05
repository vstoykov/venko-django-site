from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('blog.views',
    url(r'^$', 'blog_index', name='my_blog'),
    url(r'^(?P<category>[\w\_\-]+)/$', 'blog_index', name='my_blog_by_cat'),
    url(r'^(?P<category>[\w\_\-]+)/(?P<entry>[\w\_\-]+)/$', 'blog_entry', name='my_blog_entry'),
)
