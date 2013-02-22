from django.contrib import admin

from gallery.models import Gallery, Picture


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


admin.site.register(Picture, PictureAdmin)
admin.site.register(Gallery, GalleryAdmin)
