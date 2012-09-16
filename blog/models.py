from warnings import warn

from django.db import models
from tinymce.models import HTMLField

def truncate_smart(txt, size):
    """
    Truncate text to given size. If text is longer then add "..."
    """
    return u''.join([txt[:size], '...']) if len(txt) > size + 3 else txt


class CategoryManager(models.Manager):
    def with_entry_count(self):
        return self.annotate(entries_count=models.Count('entries'))

    def active(self):
        return self.with_entry_count().filter(entries_count__gt=0)


class Category(models.Model):
    """
    Every blog entry is put in some category
    This model describe blog entry categories
    """
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255, db_index=True)

    objects = CategoryManager()

    class Meta:
        verbose_name_plural = 'categories'

    def __unicode__(self):
        return unicode(self.title)

    @models.permalink
    def get_absolute_url(self):
        return ('my_blog_by_cat', (), {'category': self.slug})

    def get_url(self):
        """
        Deprecated method
        """
        warn("Category.get_url is deprecated", DeprecationWarning, 2)
        return self.get_absolute_url()


class EntryManager(models.Manager):
    def get_query_set(self):
        return super(EntryManager, self).get_query_set().select_related('category')


class Entry(models.Model):
    """
    This models describe every blog entry with his
    category, title, slug and content
    """
    category = models.ForeignKey(Category, related_name='entries')
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, db_index=True)
    content = HTMLField()

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    objects = EntryManager()

    class Meta:
        unique_together = (('category', 'slug',),)
        ordering = ('-created',)
        verbose_name_plural = 'entries'

    def __unicode__(self):
        return truncate_smart(self.title, 60)

    @models.permalink
    def get_absolute_url(self):
        return ('my_blog_entry', [], {'category': self.category.slug, 'entry': self.slug})

    def get_identifier(self):
        """
        Identifier used in disqus
        """
        return '%s-%s' % (self.category.slug, self.slug,)

    def get_url(self):
        """
        Deprecated method
        """
        warn("Entry.get_url is deprecated", DeprecationWarning, 2)
        return self.get_absolute_url()
