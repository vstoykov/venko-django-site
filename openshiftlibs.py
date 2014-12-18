#!/usr/bin/env python
import hashlib
import os
import json

import dj_database_url


def get_openshift_secret_token():
    """
    Gets the secret token provided by OpenShift
    or generates one (this is slightly less secure, but good enough for now)

    """
    token = os.getenv('OPENSHIFT_SECRET_TOKEN')
    if token is not None:
        return token

    name = os.getenv('OPENSHIFT_APP_NAME')
    uuid = os.getenv('OPENSHIFT_APP_UUID')
    if (name is not None and uuid is not None):
        return hashlib.sha256((name + '-' + uuid).encode('utf-8')).hexdigest()

    return None


def openshift_secure(value):
    """
    Pass a value and try to secure it with openshift secret token if available

    """
    secret_token = get_openshift_secret_token()

    if secret_token:
        return hashlib.sha256((secret_token + '-' + value).encode('utf-8')).hexdigest()
    return value


def get_cloud_config(key):
    """
    Return Python object with data stored in os environment varialbe

    """
    return json.loads(os.getenv(key) or 'null')


def get_cloud_db_settings(key):
    config = get_cloud_config(key)
    if config:
        return dj_database_url.parse(config['uri'])

def get_cloud_cache_settings(key):
    config = get_cloud_config(key)
    if config:
        return {
            'BACKEND': 'django_bmemcached.memcached.BMemcached',
            'LOCATION': config['servers'],
            'OPTIONS': {
                'username': config['username'],
                'password': config['password']
            }
        }
