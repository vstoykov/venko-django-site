import os

from .common import *
from openshiftlibs import openshift_secure, get_cloud_db_settings

BASE_DIR = os.environ['OPENSHIFT_DATA_DIR']

STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
MEDIA_URL = os.path.join(STATIC_URL, 'media/')

DATABASES = {
    'sqlite': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'site.db'),
    },
}
DATABASES['default'] = DATABASES['sqlite']

if os.getenv('OPENSHIFT_POSTGRESQL_DB_USERNAME'):
    DATABASES['postgres'] = {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['OPENSHIFT_APP_NAME'],
        'USER': os.environ['OPENSHIFT_POSTGRESQL_DB_USERNAME'],
        'PASSWORD': os.environ['OPENSHIFT_POSTGRESQL_DB_PASSWORD'],
        'HOST': os.environ['OPENSHIFT_POSTGRESQL_DB_HOST'],
        'PORT': os.environ['OPENSHIFT_POSTGRESQL_DB_PORT'],
    }
    DATABASES['default'] = DATABASES['postgres']

if os.getenv('CLOUDSQL_KEY'):
    DATABASES['cloudsql'] = get_cloud_db_settings(os.environ['CLOUDSQL_KEY'])

SECRET_KEY = openshift_secure('qi!k%l+n@hs8l8%)t@j2bl6_jj_x2q-g^em=i!6m17(7x1^$9r')
