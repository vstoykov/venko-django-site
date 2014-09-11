from django import forms
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils.translation import ugettext_lazy as _

from captcha.fields import CaptchaField

SUBJECT = getattr(settings, 'CONTACT_FORM_SUBJECT', '%(name)s want to contact you')
RECIPIENTS = getattr(settings, 'CONTACT_FORM_RECIPIENTS', ['%s<%s>' % manager for manager in settings.MANAGERS])


class ContactForm(forms.Form):
    name = forms.CharField(label=_('Name'))
    email = forms.EmailField(label=_('E-Mail'))
    message = forms.CharField(label=_('Message'), widget=forms.Textarea)

    captcha = CaptchaField(label=_('Enter the text from the image.'))

    def send_mail(self):
        data = self.cleaned_data
        email = EmailMessage(
            subject=SUBJECT % data,
            to=RECIPIENTS,
            body=_("%(name)s <%(email)s> wrote you a message:\n\n%(message)s") % data,
            headers={'Reply-To': data['email']}
        )
        email.send()
