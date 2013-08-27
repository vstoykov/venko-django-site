#!/usr/bin/env python
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "venelin.settings")

from django.core.wsgi import get_wsgi_application
from django.conf import settings
from dj_static import Cling

IP = os.environ.get('OPENSHIFT_PYTHON_IP', '0.0.0.0')
PORT = int(os.environ.get('OPENSHIFT_PYTHON_PORT', 8080))


class MediaCling(Cling):
    """
    This class is copied from https://github.com/kennethreitz/dj-static/
    When this changes came to pypi then this class can be imported from there

    """
    def __init__(self, application, base_dir=None):
        super(MediaCling, self).__init__(application, base_dir=base_dir)
        # override callable attribute with method
        self.debug_cling = self._debug_cling

    def _debug_cling(self, environ, start_response):
        environ = self._transpose_environ(environ)
        return self.cling(environ, start_response)

    def get_base_dir(self):
        return settings.MEDIA_ROOT

    def get_base_url(self):
        return settings.MEDIA_URL


def run_gevent_server(app, ip='0.0.0.0', port=8080):
   from gevent.pywsgi import WSGIServer
   http_address = '%s:%s' % (ip, port)
   print("Start gevent wsgi server at %s" % http_address)
   WSGIServer((ip, port), app).serve_forever()


def run_simple_wsgi_server(app, ip='0.0.0.0', port=8080):
    from wsgiref.simple_server import make_server
    http_address = '%s:%s' % (ip, port)
    print("Start WSGI server at %s" % http_address)
    make_server(ip, port, app).serve_forever()


def main():
    application = MediaCling(Cling(get_wsgi_application()))
    try:
        run_gevent_server(application, IP, PORT)
    except ImportError:
        run_simple_wsgi_server(application, IP, PORT)
    

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nServer stopped")
