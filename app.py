#!/usr/bin/env python
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "venelin.settings")

from django.conf import settings

IP = os.environ.get('OPENSHIFT_PYTHON_IP', '0.0.0.0')
PORT = int(os.environ.get('OPENSHIFT_PYTHON_PORT', 8080))
SOCKET_IP = os.environ.get('OPENSHIFT_PYTHON_IP', '127.0.0.1')
SOCKET_PORT = 8888
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))


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


def run_uwsgi_server(ip='0.0.0.0', port=8080):
    http_address = '%s:%s' % (ip, port)
    socket_address = '%s:%s' % (SOCKET_IP, SOCKET_PORT)
    arguments = [
        'uwsgi',
        '--socket', socket_address,
        '--http', http_address,
        '--chdir', PROJECT_DIR,
        '--wsgi-file', os.path.join(PROJECT_DIR, 'venelin/wsgi.py'),
        '--enable-threads', '--die-on-term', '--no-orphans', '--threaded-logger',
        '--master', '--workers=1', '--async=100', '--ugreen',
        '--vacuum', '--thunder-lock',
        '--static-map', '/media/=%s' % settings.MEDIA_ROOT,
        '--static-map', '/static/=%s' % settings.STATIC_ROOT,
        '--static-map', '/favicon.ico=%sfavicon.ico' % settings.STATIC_ROOT,
    ]

    os.execvp('uwsgi', arguments)


def main():
    from django.core.wsgi import get_wsgi_application
    from dj_static import Cling

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

    application = MediaCling(Cling(get_wsgi_application()))
    try:
        run_gevent_server(application, IP, PORT)
    except ImportError:
        run_simple_wsgi_server(application, IP, PORT)


if __name__ == '__main__':
    try:
        run_uwsgi_server(IP, PORT)
    except KeyboardInterrupt:
        print("\nServer stopped")
