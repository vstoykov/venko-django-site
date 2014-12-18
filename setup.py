#!/usr/bin/env python

from setuptools import setup

setup(
    name='venelins_site',
    version='1.2.2',
    description='venelin.sytes.net',
    author='Venelin Stoykov',
    author_email='vkstoykov@gmail.com',
    url='http://venelin.sytes.net/',
    install_requires=[
        'Django==1.7.1',
        'Pillow==2.6.1',
        'django-extensions>=1.4.9',
        'django-ckeditor-updated==4.4.0',
        'django-imagekit>=3.2.1',
        'django-wpadmin==1.7.0',
        'pygments',
        'appenlight-client==0.6.9',
        'psycopg2',
        'django_bmemcached==0.2.2',
    ],
)
