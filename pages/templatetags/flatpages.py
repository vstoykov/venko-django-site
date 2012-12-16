from django.template import Node, Library, TemplateSyntaxError

register = Library()


class GetFlatPagesNode(Node):
    def __init__(self, variable):
        self.variable = variable

    def render(self, context):
        from django.contrib.flatpages.models import FlatPage
        context[self.variable] = FlatPage.objects.all()
        return ''


@register.tag
def get_flatpages(parser, token):
    """
    This will store a list of available flatpages
    in the context.

    Usage::

        {% get_flatpages as flatpages %}
        {% for flatpage in flatpage %}
        ...
        {% endfor %}

    This will just pull the FlatPage.objects.all()
    and put in to variable.
    """
    args = token.contents.split()
    if len(args) != 3 or args[1] != 'as':
        raise TemplateSyntaxError("'get_flatpages' requires 'as variable' (got %r)" % args)
    return GetFlatPagesNode(args[2])
