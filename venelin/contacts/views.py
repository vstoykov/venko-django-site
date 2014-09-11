from django.shortcuts import redirect
from venelin.pages.views import flatpage

from .forms import ContactForm


def conatct_form_flatpage(request, url, redirect_url=None):
    data = request.POST if request.method == 'POST' else None
    form = ContactForm(data)
    if form.is_bound and form.is_valid():
        form.send_mail()
        return redirect(redirect_url or request.path)
    return flatpage(request, url, {'contact_form': form})
