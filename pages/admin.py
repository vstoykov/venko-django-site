from django.contrib import admin
from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.admin import FlatPageAdmin as OriginalFlatPageAdmin

class FlatPageAdmin(OriginalFlatPageAdmin):
    class Media:
        js = ('/static/ckeditor/ckeditor.js', '/static/js/ckedit.js')

try:
    admin.site.unregister(FlatPage)
except:
    pass
admin.site.register(FlatPage, FlatPageAdmin)
