from warning import warn

from django.db import models
from django.core.urlresolvers import reverse

def truncate_smart(txt, size):
    """
    Truncate text to given size. If text is longer then add "..."
    """
    return u''.join([txt[:size],'...']) if len(txt) > size + 3 else txt


class Category(models.Model):
    """
    Every blog entry is put in some category
    This model describe blog entry categories
    """
    title = models.CharField(max_length=255)
    slug  = models.SlugField(unique=True, max_length=255, db_index=True)
    
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
    
    class Meta:
        verbose_name_plural = 'categories'


class Entry(models.Model):
    """
    This models describe every blog entry with his
    category, title, slug and content
    """
    category = models.ForeignKey(Category)
    title    = models.CharField(max_length=255)
    slug     = models.SlugField(max_length=255, db_index=True)
    content  = models.TextField()    

    created  = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)    
        
    def __unicode__(self):
        return truncate_smart(self.title, 60)
    
    def get_identifier(self):
        """
        Identifier used in disqus
        """
        return '%s-%s' % ( self.category.slug, self.slug, )
    
    @models.permalink
    def get_absolute_url(self):
        return ('my_blog_entry', [], {'category': self.category.slug, 'entry': self.slug})
    
    def get_url(self):
        """
        Deprecated method
        """
        warn("Entry.get_url is deprecated", DeprecationWarning, 2)
        return self.get_absolute_url()
    
    class Meta:
        unique_together = (('category', 'slug',),)
        ordering = ('-created',)
        verbose_name_plural = 'entries'
