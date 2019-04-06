from django.urls import path

from .feeds import latest_entries_feed
from .views import blog_index, blog_entry

app_name = 'blog'
urlpatterns = [
    path('feed/', latest_entries_feed, name="feed"),
    path('<category>/', blog_index, name='category'),
    path('<category>/<entry>/', blog_entry, name='entry'),
    path('', blog_index, name='index'),
]
