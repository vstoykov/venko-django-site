from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.utils.safestring import mark_safe
from django.utils.encoding import force_str, force_text

from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFit


class GalleryManager(models.Manager):
    def active(self):
        return self.exclude(pictures=None)


class Gallery(models.Model):
    """
    Objects of this models groups pictures into galleries
    And also define where uploaded pictures will be stored
    (different folder for every gallery, based on his name)
    """
    title = models.CharField(max_length=60)
    slug = models.SlugField(max_length=60, unique=True)

    created = models.DateTimeField(auto_now_add=True, db_index=True)
    modified = models.DateTimeField(auto_now=True, db_index=True)

    objects = GalleryManager()

    class Meta:
        verbose_name_plural = 'galleries'
        ordering = ['-created', '-pk']

    def __str__(self):
        return force_str(self.title)

    def __unicode__(self):
        return force_text(self.__str__())

    @models.permalink
    def get_absolute_url(self):
        return ('gallery:gallery', (self.slug,), {})

    def get_thumbnail_url(self):
        try:
            return self.pictures.order_by('-is_album_logo', '-modified')[0].thumb.url
        except IndexError:
            return '%simg/gallery-folder.png' % settings.STATIC_URL


class Picture(models.Model):
    """
    Single picture item of given gallery.
    When new picture is uploaded it create automaticaly a thumbnail image
    for easy displaying in html page.
    """
    MAX_WIDTH = 900
    MAX_HEIGHT = 600
    MAX_THUMB_WIDTH = 130
    MAX_THUMB_HEIGHT = 100
    IMAGES_ROOT = 'gallery'

    gallery = models.ForeignKey(Gallery, related_name='pictures')
    title = models.CharField(max_length=255, blank=True, default='', help_text="Title of the picture")
    image = ProcessedImageField(max_length=255, upload_to=lambda s, name: s.upload_to(name), processors=[ResizeToFit(MAX_WIDTH, MAX_HEIGHT)], format='JPEG', options={'quality': 95})
    thumb = ImageSpecField(source='image', processors=[ResizeToFit(MAX_THUMB_WIDTH, MAX_THUMB_HEIGHT)], format='JPEG', options={'quality': 60})

    is_album_logo = models.BooleanField(default=False, help_text="If this is checked this picture will be the album logo")

    uploaded = models.DateTimeField(auto_now_add=True, db_index=True)
    modified = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        ordering = ['-uploaded', '-pk']

    def __str__(self):
        return force_str(self.title or self.image.name)

    def __unicode__(self):
        return force_text(self.__str__())

    def save(self, *args, **kwargs):
        """
        Here we do the magic of creating a thumbnail automaticaly, when new picture are set.
        """
        if not (self.pk or self.title):
            self.title = self.image.name.replace('_', ' ')
        super(Picture, self).save(*args, **kwargs)

    def upload_to(self, name=''):
        return '/'.join((self.IMAGES_ROOT, self.gallery.slug, name))

    def preview(self):
        """
        Generate html for showing thumbnail image with link to the real one.
        """
        if not self.thumb:
            return ''
        return mark_safe('<a href="{s.image.url}" title="{s.title}"><img src="{thumb.url}" width="{thumb.width}" height="{thumb.height}" alt="{s.title}" /></a>'.format(s=self, thumb=self.thumb))
    preview.allow_tags = True
