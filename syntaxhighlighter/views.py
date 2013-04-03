from django.shortcuts import render

from .forms import HighlightForm


def highlight(request, template='syntaxhighlighter/index.html'):
    data = request.POST if request.method == 'POST' else None
    form = HighlightForm(data)

    if form.is_bound and form.is_valid():
        form.do_highlight()

    return render(request, template, {'form': form})
