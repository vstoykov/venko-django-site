from django.shortcuts import render, get_object_or_404

from blog.models import Category, Entry


def blog_index(request, category=None):
    entries = Entry.objects.published()

    if category:
        category = get_object_or_404(Category, slug=category)
        entries = entries.filter(category=category)

    context = {
        'category': category,
        'entries': entries,
        'categories': Category.objects.active()
    }
    return render(request, 'blog/index.html', context)


def blog_entry(request, category, entry):
    qs = Entry.objects.all() if request.user.is_superuser else Entry.objects.published()
    entry = get_object_or_404(qs, category__slug=category, slug=entry)
    context = {
        'entry': entry,
        'category': entry.category,
        'categories': Category.objects.active(),
    }
    return render(request, 'blog/entry.html', context)
