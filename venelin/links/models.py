from __future__ import unicode_literals

from django.db import models
from django.utils.safestring import mark_safe
from django.utils.encoding import force_str, force_text
from django.utils.translation import ugettext_lazy as _


class Category(models.Model):
    """
    Links Category
    """
    title = models.CharField(_('title'), max_length=255, db_index=True)

    class Meta:
        ordering = 'title',
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __str__(self):
        return force_str(self.title)

    def __unicode__(self):
        return force_text(self.__str__())


class Link(models.Model):
    """
    This model handle a links to the world
    """
    category = models.ForeignKey(Category, verbose_name=_('category'), related_name='links')
    title = models.CharField(_('title'), max_length=255)
    url = models.CharField(_('URL'), max_length=255)

    class Meta:
        ordering = 'category',
        verbose_name = _('link')
        verbose_name_plural = _('links')

    def __str__(self):
        return force_str("{0.title} ({0.url})".format(self))

    def __unicode__(self):
        return force_text(self.__str__())

    def get_link(self):
        return mark_safe('<a href="{0.url}" target="_blank" rel="nofollow">{0.url}</a>'.format(self))
    get_link.short_description = 'url'
    get_link.admin_order_field = 'url'
    get_link.allow_tags = True
