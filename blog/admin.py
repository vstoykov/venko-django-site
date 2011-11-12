from django.contrib import admin

from blog.models import Category, Entry

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title', )}

class EntryAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'modified')
    list_display = ('title', 'slug', 'category', 'created')
    list_filter = ('category',)
    prepopulated_fields = {'slug': ('title', )}
    search_fields = ('title', 'content',)
    date_hierarchy = 'created'
    
    class Media:
        js = (
            '/media/ckeditor/ckeditor.js',
            '/media/js/ckedit.js',
        )

admin.site.register(Category, CategoryAdmin)
admin.site.register(Entry, EntryAdmin)
