from django.contrib import admin

from links.models import Category, Link


class LinkInline(admin.TabularInline):
    model = Link


class CategoryAdmin(admin.ModelAdmin):
    inlines = (LinkInline,)
    list_display = ('title',)


class LinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_link', 'category')
    list_filter = ('category',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Link, LinkAdmin)
