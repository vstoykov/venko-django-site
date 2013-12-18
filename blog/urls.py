from django.conf.urls import url, patterns

from blog.feeds import latest_entries_feed

urlpatterns = patterns('blog.views',
    url(r'^feed/$', latest_entries_feed, name="feed"),
    url(r'^(?P<category>[\w\_\-]+)/$', 'blog_index', name='category'),
    url(r'^(?P<category>[\w\_\-]+)/(?P<entry>[\w\_\-]+)/$', 'blog_entry', name='entry'),
    url(r'^$', 'blog_index', name='index'),
)
