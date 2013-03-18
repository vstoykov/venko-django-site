from django.conf import settings
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.views import redirect_to_login
from django.core.xheaders import populate_xheaders
from django.contrib.sites.models import get_current_site
from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.views import DEFAULT_TEMPLATE
from django.shortcuts import render, get_object_or_404, Http404, HttpResponsePermanentRedirect
from django.utils.safestring import mark_safe


def flatpage(request, url, extra_context=None):
    """
    Public interface to the flat page view.

    Models: `flatpages.flatpages`
    Templates: Uses the template defined by the ``template_name`` field,
        or :template:`flatpages/default.html` if template_name is not defined.
    Context:
        flatpage
            `flatpages.flatpages` object
    """
    if not url.startswith('/'):
        url = '/' + url
    site_id = get_current_site(request).id
    try:
        f = get_object_or_404(FlatPage,
            url__exact=url, sites__id__exact=site_id)
    except Http404:
        if not url.endswith('/') and settings.APPEND_SLASH:
            url += '/'
            return HttpResponsePermanentRedirect('%s/' % request.path)
        else:
            raise
    return render_flatpage(request, f, extra_context)


@csrf_protect
def render_flatpage(request, f, extra_context=None):
    """
    Internal interface to the flat page view.
    """
    # If registration is required for accessing this page, and the user isn't
    # logged in, redirect to the login page.
    if f.registration_required and not request.user.is_authenticated():
        return redirect_to_login(request.path)

    templates = [DEFAULT_TEMPLATE]
    if f.template_name:
        templates.insert(0, f.template_name)

    # To avoid having to always use the "|safe" filter in flatpage templates,
    # mark the title and content as already safe (since they are raw HTML
    # content in the first place).
    f.title = mark_safe(f.title)
    f.content = mark_safe(f.content)

    context = extra_context or {}
    context.update({
        'flatpage': f,
    })

    response = render(request, templates, context)
    populate_xheaders(request, response, FlatPage, f.id)
    return response
