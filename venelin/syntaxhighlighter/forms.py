from django import forms
from django.utils.safestring import mark_safe

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.lexers import get_all_lexers
from pygments.formatters import HtmlFormatter

LANGUAGE_CHOICES = (
    ('python', 'Pyton'),
    ('php', 'PHP'),
    ('java', 'Java'),
    ('ruby', 'Ruby'),
    ('perl', 'Perl'),
    ('c#', 'C#'),
    ('html', 'HTML'),
    ('groovy', 'Groovy'),
)

LANGUAGE_CHOICES = sorted(
    [(aliases[0], name) for (name, aliases, *__) in get_all_lexers() if aliases],
    key=lambda x: x[0],
)


class HighlightForm(forms.Form):
    lexer = forms.ChoiceField(choices=LANGUAGE_CHOICES, required=True, initial='python')
    code = forms.CharField(widget=forms.Textarea(attrs={'cols': 80, 'rows': 30}), required=True)

    def do_highlight(self):
        lexer = get_lexer_by_name(self.cleaned_data["lexer"], stripall=True)
        formatter = HtmlFormatter(linenos=True, noclasses=True)
        self.highlighted_code = mark_safe(highlight(self.cleaned_data['code'], lexer, formatter))
        #self.highlight_css = mark_safe(HtmlFormatter().get_style_defs('.source'))
