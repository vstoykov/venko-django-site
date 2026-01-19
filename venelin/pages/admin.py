from django.contrib import admin
from django.contrib.admin.exceptions import NotRegistered
from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.admin import FlatPageAdmin as OriginalFlatPageAdmin

from .forms import FlatPageForm


class FlatPageAdmin(OriginalFlatPageAdmin):
    form = FlatPageForm


try:
    admin.site.unregister(FlatPage)
except NotRegistered:
    pass
admin.site.register(FlatPage, FlatPageAdmin)
