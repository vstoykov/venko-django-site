import warnings
from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.html import format_html
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _

from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFit


def upload_picture_to(obj, name):
    return '/'.join((obj.IMAGES_ROOT, obj.gallery.slug, name))


class GalleryManager(models.Manager):

    def get_by_natural_key(self, slug):
        return self.get(slug=slug)

    def active(self):
        return self.exclude(pictures=None)


class Gallery(models.Model):
    """
    Objects of this models groups pictures into galleries
    And also define where uploaded pictures will be stored
    (different folder for every gallery, based on his name)
    """
    title = models.CharField(_('title'), max_length=60)
    slug = models.SlugField(_('slug'), max_length=60, unique=True)

    created = models.DateTimeField(_('created at'), auto_now_add=True, db_index=True)
    modified = models.DateTimeField(_('modified at'), auto_now=True, db_index=True)

    objects = GalleryManager()

    class Meta:
        ordering = '-created', '-pk',
        verbose_name = _('gallery')
        verbose_name_plural = _('galleries')

    def __str__(self):
        return force_str(self.title)

    def natural_key(self):
        return self.slug,

    def get_absolute_url(self):
        return reverse('gallery:gallery', args=(self.slug,))

    def get_thumbnail_url(self):
        try:
            return self.pictures.order_by('-is_album_logo', '-modified')[0].thumb.url
        except IndexError:
            return '%simg/gallery-folder.png' % settings.STATIC_URL


class PictureManager(models.Manager):
    def get_by_natural_key(self, image):
        return self.get(image=image)


class Picture(models.Model):
    """
    Single picture item of given gallery.
    When new picture is uploaded it create automaticaly a thumbnail image
    for easy displaying in html page.
    """
    MAX_WIDTH = 900
    MAX_HEIGHT = 600
    MAX_THUMB_WIDTH = 180
    MAX_THUMB_HEIGHT = 120
    IMAGES_ROOT = 'gallery'

    gallery = models.ForeignKey(Gallery, verbose_name=_('gallery'), related_name='pictures', on_delete=models.CASCADE)
    title = models.CharField(_('title'), max_length=255, blank=True, default='', help_text=_("Title of the picture"))
    image = ProcessedImageField(verbose_name=_('image'), max_length=255, upload_to=upload_picture_to, processors=[ResizeToFit(MAX_WIDTH, MAX_HEIGHT)], format='JPEG', options={'quality': 95})
    thumb = ImageSpecField(source='image', processors=[ResizeToFit(MAX_THUMB_WIDTH, MAX_THUMB_HEIGHT)], format='JPEG', options={'quality': 60})

    is_album_logo = models.BooleanField(_('is album logo'), default=False, help_text=_("If this is checked this picture will be the album logo"))

    uploaded = models.DateTimeField(_('uploaded at'), auto_now_add=True, db_index=True)
    modified = models.DateTimeField(_('modified at'), auto_now=True, db_index=True)

    objects = PictureManager()

    class Meta:
        ordering = '-uploaded', '-pk',
        verbose_name = _('picture')
        verbose_name_plural = _('pictures')

    def __str__(self):
        return force_str(self.title or self.image.name)

    def save(self, *args, **kwargs):
        """
        Here we do the magic of creating a thumbnail automaticaly, when new picture are set.
        """
        if not (self.pk or self.title):
            self.title = self.image.name.replace('_', ' ')
        super().save(*args, **kwargs)

    def natural_key(self):
        return str(self.image),
    natural_key.dependencies = 'gallery.gallery',

    def preview(self):
        """
        Generate html for showing thumbnail image with link to the real one.
        """
        try:
            if not self.thumb:
                return ''
        except OSError as err:
            warnings.warn(err)
            return format_html('<span class="help help-tooltip" title="{error}">N/A</span>', error=err)
        return format_html('<a href="{image_url}" title="{title}"><img src="{thumb_url}" width="{width}" height="{height}" alt="{title}" /></a>',
                           image_url=self.image.url, title=self.title, thumb_url=self.thumb.url, width=self.thumb.width, height=self.thumb.height)
    preview.short_description = _('preview')

    def as_dict(self):
        """
        Return dict representing picture data. It is used for the API
        """
        return {
            'pk': self.pk,
            'gallery': self.gallery_id,
            'title': self.title,
            'image': {
                'url': self.image.url,
                'thumbnail': self.thumb.url,
            },
        }
