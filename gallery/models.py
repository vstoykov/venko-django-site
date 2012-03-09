from django.db import models
from django.conf import settings

class Gallery(models.Model):
    """
    Objects of this models groups pictures into galleries
    And also define where uploaded pictures will be stored
    (different folder for every gallery, based on his name)
    """
    GALLERIES_DIR  = 'gallery/'
    
    title   = models.CharField(max_length=60)
    slug    = models.SlugField(max_length=60, unique=True)
    
    created  = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True) 
    
    def __unicode__(self):
        return unicode(self.title)
    
    class Meta:
        verbose_name_plural = 'galleries'

    @models.permalink
    def get_absolute_url(self):
        return ('gallery', (self.slug,), {})


    def get_dir(self): return '%s%s/' % (self.GALLERIES_DIR, self.slug)
    def get_thumb_dir(self): return '%sthumbs/' % self.get_dir()
    
    def get_thumbnail(self):
        try:
            return self.pictures.all()[0].thumb.url
        except:
            return '%simg/gallery-folder.png' % settings.MEDIA_URL


class Picture(models.Model):
    """
    Single picture item of given gallery.
    When new picture is uploaded it create automaticaly a thumbnail image
    for easy displaying in html page.
    """
    MAX_WIDTH   = 900
    MAX_HEIGHT  = 600
    MAX_THUMB_WIDTH  = 130
    MAX_THUMB_HEIGHT = 100
    
    def get_upload_to(self, name=''): return '%s%s' % (self.gallery.get_dir(), name)
    def get_upload_thumb_to(self, name=''): return '%s%s' % (self.gallery.get_thumb_dir(), name)
    
    gallery = models.ForeignKey(Gallery, related_name='pictures')
    title   = models.CharField(max_length=255, blank=True, default='', help_text="Title of the picture")
    image   = models.ImageField(max_length=255, upload_to=get_upload_to)
    thumb   = models.ImageField(max_length=255, upload_to=get_upload_thumb_to, blank=True, null=True, editable=False)
    
    is_album_logo = models.BooleanField(default=False, help_text="If this is checked this picture will be the album logo")
    
    uploaded = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return unicode(self.title if self.title else self.image.name)
    
    def preview(self):
        """
        Generate html for showing thumbnail image with link to the real one.
        """
        thumb = self.thumb
        if not thumb:
            return ''
        return '<a href="%s"><img src="%s" width="%s" height="%s" alt="" /></a>' % (self.image.url, thumb.url, thumb.width, thumb.height,)
    preview.allow_tags = True
    
    def save(self, *args, **kwargs):
        """
        Here we do the magic of creating a thumbnail automaticaly, when new picture are set.
        """
        committed = self.image._committed
        if not committed:
            # New picture has been uploaded. We must create a thumbnail for that image
            
            filename = self.image.name
            if not self.title:
                self.title = filename.replace('_', ' ')

            # Duplicate main image into thumb. Resizing will be done after saving
            self.thumb.name = self.image.name
            self.thumb.file = self.image.file
            self.thumb._committed = False
            
        super(self.__class__, self).save(*args, **kwargs)
        
        if not committed:
            # Start Real resizing
            import Image
            image = Image.open(self.image.path)
            
            # Reduse size of main large image.
            image.thumbnail((self.MAX_WIDTH, self.MAX_HEIGHT), Image.ANTIALIAS)
            image.save(self.image.path, image.format)
            
            # Create thumbnail                
            image.thumbnail((self.MAX_THUMB_WIDTH, self.MAX_THUMB_HEIGHT), Image.ANTIALIAS)
            image.save(self.thumb.path, image.format)
