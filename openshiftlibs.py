#!/usr/bin/env python
import hashlib
import os


def get_openshift_secret_token():
    """
    Gets the secret token provided by OpenShift
    or generates one (this is slightly less secure, but good enough for now)

    """
    token = os.getenv('OPENSHIFT_SECRET_TOKEN')
    name = os.getenv('OPENSHIFT_APP_NAME')
    uuid = os.getenv('OPENSHIFT_APP_UUID')
    if token is not None:
        return token
    elif (name is not None and uuid is not None):
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
