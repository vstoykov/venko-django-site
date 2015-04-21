from django.core.cache import caches
from django.dispatch import receiver
from django.db.models.signals import post_save, m2m_changed, post_delete
from django.contrib.flatpages.models import FlatPage

from .blog.models import Entry
from .gallery.models import Picture
from .links.models import Link


def get_pages_cache():
    try:
        return caches['pages']
    except KeyError:
        try:
            return caches['default']
        except KeyError:
            return None


def invalidate_cache(**kwargs):
    if kwargs['sender'] in [FlatPage, Entry, Picture, Link]:
        cache = get_pages_cache()
        if cache:
            cache.clear()

for signal in [post_save, m2m_changed, post_delete]:
    receiver(signal)(invalidate_cache)
