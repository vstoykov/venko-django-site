from django.conf.urls import url, patterns

from blog.feeds import latest_entries_feed

urlpatterns = patterns('blog.views',
    url(r'^feed/$', latest_entries_feed, name="blog_feed"),
    url(r'^(?P<category>[\w\_\-]+)/$', 'blog_index', name='my_blog_by_cat'),
    url(r'^(?P<category>[\w\_\-]+)/(?P<entry>[\w\_\-]+)/$', 'blog_entry', name='my_blog_entry'),
    url(r'^$', 'blog_index', name='my_blog'),
)
