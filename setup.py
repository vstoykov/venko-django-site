#!/usr/bin/env python

from setuptools import setup

setup(
    name='venelins_site',
    version='1.2.3',
    description='venelin.sytes.net',
    author='Venelin Stoykov',
    author_email='vkstoykov@gmail.com',
    url='http://venelin.sytes.net/',
    install_requires=[
        'Django==1.7.7',
        'Pillow==2.7.0',
        'django-extensions>=1.5.2',
        'django-ckeditor-updated==4.4.0',
        'django-imagekit>=3.2.6',
        'django-wpadmin==1.7.2',
        'Pygments',
        'appenlight-client==0.6.12',
        'psycopg2',
        'django_bmemcached==0.2.2',
    ],
)
