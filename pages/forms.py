from django import forms
from django.contrib.flatpages.models import FlatPage
from tinymce.widgets import TinyMCE

from .utils import get_flaptage_template_choices


class FlatPageForm(forms.ModelForm):

    class Meta:
        model = FlatPage
        widgets = {
            'content': TinyMCE(attrs={'cols': 80, 'rows': 30}),
            'template_name': forms.Select(choices=get_flaptage_template_choices())
        }
