from django.db import models
from django.db.models import Count, Max, When, Case
from django.template.defaultfilters import striptags, truncatechars
from django.urls import reverse
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _

from ckeditor.fields import RichTextField


class CategoryManager(models.Manager):

    def get_by_natural_key(self, slug):
        return self.get(slug=slug)

    def with_entry_count(self):
        return self.annotate(entries_count=Count(Case(When(entries__is_published=True, then=1))))

    def active(self):
        return self.with_entry_count().filter(entries_count__gt=0).order_by('-entries_count')

    def with_last_modified(self):
        return self.annotate(
            modified=Max(Case(When(entries__is_published=True, then='entries__created')))
        ).exclude(modified=None).order_by('-modified')


class Category(models.Model):
    """
    Every blog entry is put in some category
    This model describe blog entry categories
    """
    title = models.CharField(_('title'), max_length=255)
    slug = models.SlugField(_('slug'), unique=True, max_length=255, db_index=True)

    objects = CategoryManager()

    class Meta:
        ordering = 'title',
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __str__(self):
        return force_str(self.title)

    def natural_key(self):
        return self.slug,

    def get_absolute_url(self):
        return reverse('blog:category', kwargs={'category': self.slug})


class EntryManager(models.Manager):

    def get_queryset(self):
        return super(EntryManager, self).get_queryset().select_related('category')

    def get_by_natural_key(self, slug):
        return self.get(slug=slug)

    def published(self):
        return self.filter(is_published=True)


class Entry(models.Model):
    """
    This models describe every blog entry with his
    category, title, slug and content
    """
    category = models.ForeignKey(Category, verbose_name=_('category'), related_name='entries', on_delete=models.PROTECT)
    title = models.CharField(_('title'), max_length=255)
    slug = models.SlugField(_('slug'), max_length=255, db_index=True)
    content = RichTextField(_('content'))

    seo_keywords = models.CharField(_('keywords'), max_length=128, blank=True, default='')
    seo_description = models.CharField(_('description'), max_length=256, blank=True, default='')

    created = models.DateTimeField(_('created at'), auto_now_add=True, db_index=True)
    modified = models.DateTimeField(_('modified at'), auto_now=True, db_index=True)
    is_published = models.BooleanField(_('is published'), default=False)

    objects = EntryManager()

    class Meta:
        unique_together = 'category', 'slug',
        ordering = '-created',
        verbose_name = _('entry')
        verbose_name_plural = _('entries')

    def __str__(self):
        return force_str(truncatechars(self.title, 60))

    def natural_key(self):
        return self.slug,
    natural_key.dependencies = ['blog.category']

    def get_absolute_url(self):
        return reverse('blog:entry', kwargs={'category': self.category.slug, 'entry': self.slug})

    def get_identifier(self):
        """
        Identifier used in disqus
        """
        return '%s-%s' % (self.category.slug, self.slug,)

    def get_seo_description(self):
        return self.seo_description or truncatechars(striptags(self.content), 200).replace('\n', ' ').replace('\r', '')
