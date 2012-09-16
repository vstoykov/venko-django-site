from django.contrib import admin

from blog.models import Category, Entry


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title', )}


class EntryAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'modified')
    list_display = ('title', 'slug_as_link', 'category', 'created')
    list_filter = ('category',)
    prepopulated_fields = {'slug': ('title', )}
    search_fields = ('title', 'content',)
    date_hierarchy = 'created'

    def slug_as_link(self, obj):
        return '<a href="%s">%s</a>' % (obj.get_absolute_url(), obj.slug)
    slug_as_link.allow_tags = True

admin.site.register(Category, CategoryAdmin)
admin.site.register(Entry, EntryAdmin)
