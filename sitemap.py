from django.contrib.sitemaps import FlatPageSitemap, GenericSitemap

from blog.models import Entry
from gallery.models import Gallery

blog_dict = {
    'queryset': Entry.objects.all(),
    'date_field': 'modified',
}

gallery_dict = {
    'queryset': Gallery.objects.all(),
    'date_field': 'modified',
}

sitemaps = {
    'flatpages': FlatPageSitemap,
    'blog': GenericSitemap(blog_dict, priority=0.9),
    'gallery': GenericSitemap(gallery_dict, priority=0.6),
}
