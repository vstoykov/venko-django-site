#!/usr/bin/env python3

import sys
from setuptools import setup

needs_pytest = bool({'pytest', 'test', 'ptr'}.intersection(sys.argv))

setup(
    name='venelin-site',
    version='2.1.1',
    description='Simple Personal WEB site made with Django',
    author='Venelin Stoykov',
    author_email='vkstoykov@gmail.com',
    url='https://stoykov.tk/',
    setup_requires=['pytest-runner'] if needs_pytest else [],
    install_requires=[
        'Django>=2.2,<3',
        'Pillow>=4.3.0',
        'pilkit>=2.0',
        'django-ckeditor>=5.4.0,<7.0',
        'django-extensions>=3.0.6,<4',
        'django-appconf>=1.0.1',
        'django-imagekit>=4.0.1',
        'social-auth-core[openidconnect]>=3.0',
        'social-auth-app-django>=3.1',
        'Pygments',
        'appenlight-client>=0.6.25',
        'psycopg2',
    ],
    tests_require=['pytest-django'],
)
