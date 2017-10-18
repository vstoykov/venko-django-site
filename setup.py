#!/usr/bin/env python

from setuptools import setup

setup(
    name='venelin-site',
    version='1.3.0',
    description='venelin.sytes.net',
    author='Venelin Stoykov',
    author_email='vkstoykov@gmail.com',
    url='http://venelin.sytes.net/',
    install_requires=[
        'Django>=1.8.18,<1.12',
        'Pillow==4.1.1',
        'pilkit>=2.0',
        'django-ckeditor==5.2.2',
        'django-extensions==1.7.9',
        'django-appconf>=1.0.1',
        'django-imagekit>=4.0.1',
        'Pygments',
        'appenlight-client==0.6.21',
        'psycopg2',
    ],
)
