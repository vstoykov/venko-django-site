#!/usr/bin/env python

from setuptools import setup

setup(
    name='venelins_site',
    version='1.2.0',
    description='venelin.sytes.net',
    author='Venelin Stoykov',
    author_email='vkstoykov@gmail.com',
    url='http://venelin.sytes.net/',
    install_requires=[
        'Django==1.6.5',
        'Pillow==2.4.0',
        'South>=0.8.4',
        'django-extensions>=1.3.7',
        'django-ckeditor-updated==4.4.0',
        'django-imagekit>=3.2.1',
        'django_admin_bootstrapped',
        'pygments',
        #'uWSGI>=2.0.0',
        'psycopg2',
    ],
)
