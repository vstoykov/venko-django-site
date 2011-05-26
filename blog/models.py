from django.db import models
from django.core.urlresolvers import reverse

class Category(models.Model):
    title = models.CharField(max_length=255)
    slug  = models.SlugField(unique=True, max_length=255, db_index=True)
    
    def __unicode__(self):
        return unicode(self.title)
    
    def get_url(self):
        return reverse('my_blog_by_cat', kwargs={'category': self.slug,})
    
    class Meta:
        verbose_name_plural = 'categories'


class Entry(models.Model):
    category = models.ForeignKey(Category)
    title    = models.CharField(max_length=255)
    slug     = models.SlugField(max_length=255, db_index=True)
    content  = models.TextField()    

    created  = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)    
        
    def __unicode__(self):
        return u'%s%s' % (self.title[:60], '...' if len(self.title) > 60 else '')
    
    def get_identifier(self):
        return '%s-%s' % ( self.category.slug, self.slug, )
    
    def get_absolute_url(self):
        return self.get_url()
    
    def get_url(self):
        return reverse('my_blog_entry', kwargs={'category': self.category.slug, 'entry': self.slug})
    
    class Meta:
        unique_together = (('category', 'slug',),)
        ordering = ('-created',)
        verbose_name_plural = 'entries'