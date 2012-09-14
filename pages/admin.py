from django.contrib import admin
from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.admin import FlatPageAdmin as OriginalFlatPageAdmin
from django.conf import settings


class FlatPageAdmin(OriginalFlatPageAdmin):
    class Media:
        js = (
            '%sckeditor/ckeditor.js' % settings.STATIC_URL,
            '%sjs/ckedit.js' % settings.STATIC_URL,
        )

try:
    admin.site.unregister(FlatPage)
except:
    pass
admin.site.register(FlatPage, FlatPageAdmin)
