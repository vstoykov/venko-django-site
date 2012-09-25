import os
from itertools import chain

from django.conf import settings
from django.utils.importlib import import_module

APP_DIRS = [os.path.dirname(import_module(app).__file__) for app in settings.INSTALLED_APPS]


def get_flatpage_templates():
    apps_templates = [os.listdir(path) for path in (
                        "%s/templates/flatpages" % app_dir for app_dir in APP_DIRS
                    ) if os.path.exists(path)]

    site_templates = [os.listdir(path) for path in (
                        "%s/flatpages" % tmp_dir.rstrip('/') for tmp_dir in settings.TEMPLATE_DIRS
                    ) if os.path.exists(path)]

    return sorted(tmp for tmp in chain(*(apps_templates + site_templates)) if tmp.endswith('.html'))


def get_flaptage_template_choices():
    return [(
            "flatpages/%s" % tmp,
            tmp.replace('.html', '')
        ) for tmp in get_flatpage_templates()]
