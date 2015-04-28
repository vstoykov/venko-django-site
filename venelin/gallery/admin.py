from django.contrib import admin
from django.contrib.admin.utils import unquote
from django.core.exceptions import PermissionDenied
from django.utils.decorators import method_decorator
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _
from django.utils.html import escape
from django.http import Http404
from django.views.decorators.http import require_POST

from .models import Gallery, Picture
from .forms import UploadPictureForm
from .ajax import JSONResponse, JSONResponseBadRequest


class PictureAdmin(admin.ModelAdmin):
    readonly_fields = ('preview', 'uploaded', 'modified', )
    list_display = ('title', 'preview', 'gallery')
    list_filter = ('gallery',)
    date_hierarchy = 'uploaded'


class PictureInline(admin.TabularInline):
    model = Picture
    readonly_fields = ('preview',)
    fields = ('preview', 'is_album_logo', 'title', )
    extra = 0
    show_change_link = True


class GalleryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created', 'modified',)
    inlines = (PictureInline,)
    date_hierarchy = 'created'
    list_display = ('title', 'slug')

    class Media:
        css = {
            'screen': (
                'css/gallery.admin.css',
            )
        }
        js = (
            'js/jquery.ui.widget.js',
            'js/jquery.fileupload.js',
            'js/gallery.admin.js',
        )

    def get_urls(self):
        from django.conf.urls import url
        info = self.model._meta.app_label, self.model._meta.model_name

        urlpatterns = [
            url(r'^(?P<object_id>\d+)/upload/$',
                self.admin_site.admin_view(self.upload_image),
                name='%s_%s_upload' % info),
        ]
        urlpatterns.extend(super(GalleryAdmin, self).get_urls())

        return urlpatterns

    @method_decorator(require_POST)
    def upload_image(self, request, object_id):
        gallery = self.get_object(request, unquote(object_id))

        if gallery is None:
            raise Http404(_('%(name)s object with primary key %(key)r does not exist.') % {
                'name': force_text(self.model._meta.verbose_name),
                'key': escape(object_id),
            })

        if not self.has_change_permission(request, gallery):
            raise PermissionDenied

        form = UploadPictureForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.gallery = gallery
            instance = form.save()
            self.log_change(request, gallery, _('Added %(name)s "%(object)s".') % {
                'name': force_text(instance._meta.verbose_name),
                'object': force_text(instance),
            })
            return JSONResponse({'picture': form.instance.as_dict()})
        return JSONResponseBadRequest({'errors': form.errors})


admin.site.register(Picture, PictureAdmin)
admin.site.register(Gallery, GalleryAdmin)
