from django import forms
from django.contrib.flatpages.models import FlatPage
from django_prose_editor.fields import ProseEditorFormField, AdminProseEditorWidget

from .utils import get_flatpage_template_choices


class FlatPageForm(forms.ModelForm):

    content = ProseEditorFormField(
        widget=AdminProseEditorWidget
    )

    class Meta:
        model = FlatPage
        fields = '__all__'
        widgets = {
            'template_name': forms.Select(choices=get_flatpage_template_choices()),
            'sites': forms.CheckboxSelectMultiple,
        }
