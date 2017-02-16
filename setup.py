#!/usr/bin/env python

from setuptools import setup

setup(
    name='venelin-site',
    version='1.2.3',
    description='venelin.sytes.net',
    author='Venelin Stoykov',
    author_email='vkstoykov@gmail.com',
    url='http://venelin.sytes.net/',
    install_requires=[
        'Django==1.8.7',
        'Pillow==4.0.0',
        'django-ckeditor==4.5.1',
        'django-extensions==1.6.1',
        'django-appconf>=1.0.1',
        'django-imagekit>=3.3',
        'django-wpadmin==1.7.4',
        'Pygments',
        'appenlight-client==0.6.15',
        'psycopg2',
    ],
)
