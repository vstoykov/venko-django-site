# -*- coding: utf-8 -*-
from django.contrib.syndication.views import Feed

from blog.models import Category, Entry


class LatestEntriesFeed(Feed):
    title = u"Статии от блога на Венелин Стойков"
    link = "/blog/feed/"
    description = u"Последните 10 статии от блога на Венелин Стойков"

    def items(self):
        return Entry.objects.order_by('-created')[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content

latest_entries_feed = LatestEntriesFeed()
