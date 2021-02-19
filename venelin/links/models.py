from django.db import models
from django.utils.html import format_html
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _


class CategoryManager(models.Manager):

    def get_by_natural_key(self, title):
        return self.get(title=title)


class Category(models.Model):
    """
    Links Category
    """
    title = models.CharField(_('title'), max_length=255, db_index=True)

    objects = CategoryManager()

    class Meta:
        ordering = 'title',
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __str__(self):
        return force_str(self.title)

    def natural_key(self):
        return self.title,


class LinkManager(models.Manager):

    def get_by_natural_key(self, title):
        return self.get(title=title)


class Link(models.Model):
    """
    This model handle a links to the world
    """
    category = models.ForeignKey(Category, verbose_name=_('category'), related_name='links', on_delete=models.CASCADE)
    title = models.CharField(_('title'), max_length=255)
    url = models.CharField(_('URL'), max_length=255)

    objects = LinkManager()

    class Meta:
        ordering = 'category',
        verbose_name = _('link')
        verbose_name_plural = _('links')

    def __str__(self):
        return force_str("{0.title} ({0.url})".format(self))

    def natural_key(self):
        return self.url,
    natural_key.dependencies = 'links.category',

    def get_link(self):
        return format_html('<a href="{url}" target="_blank" rel="nofollow">{url}</a>', url=self.url)
    get_link.short_description = 'url'
    get_link.admin_order_field = 'url'
