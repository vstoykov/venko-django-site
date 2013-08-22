from __future__ import unicode_literals

from django.db import models
from django.utils.safestring import mark_safe


class Category(models.Model):
    """
    Links Category
    """
    title = models.CharField(max_length=255, db_index=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __unicode__(self):
        return self.title


class Link(models.Model):
    """
    This model handle a links to the world
    """
    category = models.ForeignKey(Category, related_name='links')
    title = models.CharField(max_length=255)
    url = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Link'
        verbose_name_plural = 'Links'
        ordering = ('category',)

    def __unicode__(self):
        return "%s (%s)" % (self.title, self.url)

    def get_link(self):
        return mark_safe('<a href="{0.url}" target="_blank" rel="nofollow">{0.url}</a>'.format(self))
    get_link.short_description = 'url'
    get_link.admin_order_field = 'url'
    get_link.allow_tags = True
