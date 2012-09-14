from django.shortcuts import render, get_object_or_404

from blog.models import Category, Entry


def blog_index(request, category=None):
    context = {
        'category': category,
        'entries': Entry.objects.order_by('-created'),
        'categories': Category.objects.active()
    }
    if category:
        context.update({
            'category': get_object_or_404(Category, slug=category),
            'entries': context['entries'].filter(category=category)
        })
    return render(request, 'blog/index.html', context)


def blog_entry(request, category, entry):
    entry = get_object_or_404(Entry, category__slug=category, slug=entry)
    context = {
        'entry': entry,
        'category': entry.category,
        'categories': Category.objects.active(),
    }
    return render(request, 'blog/entry.html', context)
