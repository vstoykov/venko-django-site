import os
from itertools import chain

from django.conf import settings
from django.template.loaders.app_directories import app_template_dirs


def get_flatpage_templates():
    flatpages_dirs = (
        os.path.join(path, "flatpages")
        for path in chain(settings.TEMPLATE_DIRS, app_template_dirs)
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
