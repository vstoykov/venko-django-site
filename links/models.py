from django.db import models

class Category(models.Model):
    """
    Links Category
    """
    title = models.CharField(max_length=255)
    
    def __unicode__(self):
        return unicode(self.title)
    
    class Meta:
        verbose_name_plural = 'categories'


class Link(models.Model):
    """
    This model handle a links to the world
    """
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=255)
    url   = models.CharField(max_length=255)
