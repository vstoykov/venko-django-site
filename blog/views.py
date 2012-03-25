from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404

from blog.models import Category, Entry


def blog_index(request, category=None):
    entries = Entry.objects.order_by('-created')
    if category:
        category = get_object_or_404(Category, slug=category)
        entries = entries.filter(category=category)
    categories = Category.objects.exclude(entry=None)
    return render_to_response('blog/index.html', locals(), RequestContext(request))
    
def blog_entry(request, category, entry):
    entry = get_object_or_404(Entry, category__slug=category, slug=entry)
    category = entry.category
    categories = Category.objects.exclude(entry=None)
    
    return render_to_response('blog/entry.html', locals(), RequestContext(request))


