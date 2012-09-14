from django.contrib import admin

from links.models import Category, Link


class LinkInline(admin.TabularInline):
    model = Link


class CategoryAdminInline(admin.ModelAdmin):
    inlines = (LinkInline,)


class LinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'category')
    list_filter = ('category',)


admin.site.register(Category, admin.ModelAdmin)
admin.site.register(Link, LinkAdmin)
