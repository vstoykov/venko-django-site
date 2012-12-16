from django.template import Library
from blog.models import Entry

register = Library()


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
