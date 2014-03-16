from django import forms
from django.contrib.flatpages.models import FlatPage
from ckeditor.fields import RichTextFormField

from .utils import get_flaptage_template_choices


class FlatPageForm(forms.ModelForm):

    content = RichTextFormField()

    class Meta:
        model = FlatPage
        widgets = {
            'template_name': forms.Select(choices=get_flaptage_template_choices())
        }
