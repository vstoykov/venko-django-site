#!/usr/bin/env python

from setuptools import setup

setup(
    name='venelins_site',
    version='1.0.1',
    description='venelin.sytes.net',
    author='Venelin Stoykov',
    author_email='vkstoykov@gmail.com',
    url='http://venelin.sytes.net/',
    install_requires=[
        'Django>=1.6',
        'Pillow>=2.1.0',
        'South>=0.8.2',
        'django-extensions>=1.2.0',
        'django-tinymce>=1.5.2',
        'django-imagekit>=3.0.3',
        'django-admin-tools',
        'pygments',
        'uWSGI>=2.0.0',
        #'gevent',
        #'dj-static',
        'psycopg2',
    ],
)
