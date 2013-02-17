from django.db import models


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
