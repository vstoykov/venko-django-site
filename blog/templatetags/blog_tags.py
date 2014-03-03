from django.core.exceptions import ImproperlyConfigured
from django.contrib.sites.models import Site
from django.conf import settings
from django.template import Library

from blog.models import Entry

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
    latest = list(Entry.objects.order_by('-created')[:n + 1])
    context.update({
        'latest': latest[:n],
        'show_more_link': len(latest) == n + 1
    })
    return context


@register.simple_tag
def disqus_dev():
    """
    Return the HTML/js code to enable DISQUS comments on a local
    development server if settings.DEBUG is True.

    """
    if settings.DEBUG:
        domain = Site.objects.get_current().domain
        return '\n'.join([
            '<script type="text/javascript">',
            '\tvar disqus_developer = 1;',
            '\tvar disqus_url = "http://%s/";' % domain,
            '</script>'
        ])
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
