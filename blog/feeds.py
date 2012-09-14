# -*- coding: utf-8 -*-
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords_html

from blog.models import Entry


class EntriesFeed(Feed):
    title = u"Статии от блога на Венелин Стойков"
    link = "/blog/feed/"
    description = u"Всички статии от блога на Венелин Стойков"

    def items(self):
        return Entry.objects.select_related('category').order_by('-created')

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords_html(item.content, 80)


class LatestEntriesFeed(EntriesFeed):
    description = u"Последните 10 статии от блога на Венелин Стойков"

    def items(self):
        return super(LatestEntriesFeed, self).items()[:10]


latest_entries_feed = LatestEntriesFeed()
