from django import forms

from .models import Picture


class UploadPictureForm(forms.ModelForm):
    class Meta:
        model = Picture
        fields = 'image',
