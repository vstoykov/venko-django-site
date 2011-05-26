from django.contrib.sitemaps import FlatPageSitemap, GenericSitemap
from blog.models import Entry

blog_dict = {
    'queryset': Entry.objects.all(),
    'date_field': 'created',
}

sitemaps = {
    'flatpages': FlatPageSitemap,
    'blog': GenericSitemap(blog_dict, priority=0.6),
}