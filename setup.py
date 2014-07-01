#!/usr/bin/env python

from setuptools import setup

setup(
    name='venelins_site',
    version='1.2.1',
    description='venelin.sytes.net',
    author='Venelin Stoykov',
    author_email='vkstoykov@gmail.com',
    url='http://venelin.sytes.net/',
    install_requires=[
        'Django==1.7c2',
        'Pillow==2.4.0',
        'django-extensions>=1.3.8',
        'django-ckeditor-updated==4.4.0',
        'django-imagekit>=3.2.1',
        'django-wpadmin>=1.6.1,<1.7',
        'pygments',
        'appenlight-client==0.6.9',
        'psycopg2',
    ],
)
