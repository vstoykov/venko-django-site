from django.core.exceptions import ImproperlyConfigured
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.template import Library
from django.utils.html import format_html

from ...models import Entry

register = Library()


try:
    WEBSITE_SHORTNAME = settings.DISQUS_WEBSITE_SHORTNAME
except AttributeError:
    raise ImproperlyConfigured('You need set `DISQUS_WEBSITE_SHORTNAME` in your settings')


@register.inclusion_tag('blog/latest_entries.html', takes_context=True)
def latest_entries(context, n):
    """
    Render latest n entries from blog

    Usage:

        {% latest_entries n %}

    """
    latest = list(Entry.objects.published().order_by('-created')[:n + 1])
    context.update({
        'latest': latest[:n],
        'show_more_link': len(latest) == n + 1
    })
    return context


@register.simple_tag(takes_context=True)
def disqus_dev(context):
    """
    Return the HTML/js code to enable DISQUS comments on a local
    development server if settings.DEBUG is True.

    """
    if settings.DEBUG:
        site = get_current_site(context.request)
        return format_html(
            '<script type="text/javascript">'
            'var disqus_developer=1, disqus_url="http://{domain}/";'
            '</script>',
            domain=site.domain,
        )
    return ""


@register.inclusion_tag('blog/tags/show_comments.html')
def show_comments():
    """
    Return the HTML code to display DISQUS comments.

    """
    return {'shortname': WEBSITE_SHORTNAME}


@register.inclusion_tag('blog/tags/num_replies.html')
def num_replies():
    """
    Return the HTML/js code which transforms links that end with an
    #disqus_thread anchor into the threads comment count.

    """
    return {'shortname': WEBSITE_SHORTNAME}
