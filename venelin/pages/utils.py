import os
from itertools import chain

from django.conf import settings
from django.template.loaders.app_directories import get_app_template_dirs


def get_flatpage_templates():
    flatpages_dirs = (
        os.path.join(path, "flatpages")
        for path in chain(get_template_dirs(), get_app_template_dirs('templates'))
        if os.path.exists(os.path.join(path, "flatpages"))
    )

    return sorted(set(
        tmp
        for path in flatpages_dirs for tmp in os.listdir(path)
        if tmp.endswith('.html')
    ))


def get_flatpage_template_choices():
    return [(
            os.path.join("flatpages", tmp),
            tmp.replace('.html', '')
            ) for tmp in get_flatpage_templates()]


def get_template_dirs():
    for backend in settings.TEMPLATES:
        for path in backend.get('DIRS', []):
            yield path
