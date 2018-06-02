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
    cache = get_pages_cache()
    if cache:
        cache.clear()


# Register Receivers for for cleaning the cache
_signals = (post_save, m2m_changed, post_delete)
for _model in (FlatPage, Entry, Picture, Link):
    receiver(_signals, sender=_model)(invalidate_cache)
del _signals
del _model
