from django.contrib.sitemaps import FlatPageSitemap, GenericSitemap

from .blog.models import Entry, Category
from .gallery.models import Gallery


sitemaps = {
    'flatpages': FlatPageSitemap,
    'blog_entries': GenericSitemap(
        {
            'queryset': Entry.objects.published(),
            'date_field': 'modified',
        },
        priority=0.9
    ),
    'blog_categories': GenericSitemap(
        {
            'queryset': Category.objects.with_last_modified(),
            'date_field': 'modified',
        },
        priority=0.8
    ),
    'gallery': GenericSitemap(
        {
            'queryset': Gallery.objects.active(),
            'date_field': 'modified',
        },
        priority=0.6
    ),
}
