from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html

from .models import Category, Entry
from .forms import EntryAdminForm


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title', )}


class EntryAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'modified')
    list_display = ('title', 'slug_as_link', 'category_as_link', 'created', 'is_published')
    list_filter = ('is_published', 'category',)
    prepopulated_fields = {'slug': ('title', )}
    search_fields = ('title', 'content',)
    actions = ('publish_selected', 'unpublish_selected',)
    date_hierarchy = 'created'

    form = EntryAdminForm

    def get_queryset(self, request):
        return super(EntryAdmin, self).get_queryset(request).select_related('category')

    def slug_as_link(self, obj):
        return format_html('<a href="{}">{}</a>', obj.get_absolute_url(), obj.slug)
    slug_as_link.admin_order_field = 'slug'
    slug_as_link.short_description = _('slug')

    def category_as_link(self, obj):
        return format_html('<a href="{}">{}</a>', obj.category.get_absolute_url(), obj.category)
    category_as_link.admin_order_field = 'category'
    category_as_link.short_description = _('category')

    def publish_selected(self, request, queryset):
        count = queryset.filter(is_published=False).update(is_published=True)
        self.message_user(request, '%s entries was successfully published' % count)
    publish_selected.short_description = _('Publish selected entries')

    def unpublish_selected(self, request, queryset):
        count = queryset.filter(is_published=True).update(is_published=False)
        self.message_user(request, '%s entries was successfully unpublished' % count)
    unpublish_selected.short_description = _('Unpublish selected entries')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Entry, EntryAdmin)
