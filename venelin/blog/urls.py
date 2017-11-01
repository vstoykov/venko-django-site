from django.conf.urls import url

from .feeds import latest_entries_feed
from .views import blog_index, blog_entry

app_name = 'blog'
urlpatterns = [
    url(r'^feed/$', latest_entries_feed, name="feed"),
    url(r'^(?P<category>[\w\_\-]+)/$', blog_index, name='category'),
    url(r'^(?P<category>[\w\_\-]+)/(?P<entry>[\w\_\-]+)/$', blog_entry, name='entry'),
    url(r'^$', blog_index, name='index'),
]
