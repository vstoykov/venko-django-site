from django.contrib import admin
from django.utils.decorators import method_decorator
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

    extra = 0


class GalleryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created', 'modified',)
    inlines = (PictureInline,)
    date_hierarchy = 'created'
    list_display = ('title', 'slug')

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
        gallery = self.get_object(request, object_id)
        form = UploadPictureForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.gallery = gallery
            form.save()
            return JSONResponse({'picture': form.instance.as_dict()})
        return JSONResponseBadRequest({'errors': form.errors})


admin.site.register(Picture, PictureAdmin)
admin.site.register(Gallery, GalleryAdmin)
