import os

from django.views.static import serve, Http404
from django.conf import settings
from django.db import connection



def terminal_width():
    """
    Function to compute the terminal width.
    WARNING: This is not my code, but I've been using it forever and
    I don't remember where it came from.
    """
    width = 0
    try:
        import struct
        import fcntl
        import termios
        s = struct.pack('HHHH', 0, 0, 0, 0)
        x = fcntl.ioctl(1, termios.TIOCGWINSZ, s)
        width = struct.unpack('HHHH', x)[1]
    except:
        pass
    if width <= 0:
        try:
            width = int(os.environ['COLUMNS'])
        except:
            pass
    if width <= 0:
        width = 80
    return width


class SQLPrintingMiddleware(object):
    """
    Middleware which prints out a list of all SQL queries done
    for each view that is processed. This is only useful for debugging.
    """
    def process_response(self, request, response):
        if not settings.DEBUG or len(connection.queries) == 0 \
            or request.path_info.startswith('/favicon.ico') \
            or request.path_info.startswith(settings.STATIC_URL) \
                or request.path_info.startswith(settings.MEDIA_URL):
            return response

        indentation = 2
        print "\n\n%s\033[1;35m[SQL Queries for]\033[1;34m %s\033[0m\n" % (" " * indentation, request.path_info)
        width = terminal_width()
        total_time = 0.0
        for query in connection.queries:
            nice_sql = query['sql'].replace('"', '').replace(',', ', ')
            sql = "\033[1;31m[%s]\033[0m %s" % (query['time'], nice_sql)
            total_time = total_time + float(query['time'])
            while len(sql) > width - indentation:
                print "%s%s" % (" " * indentation, sql[:width - indentation])
                sql = sql[width - indentation:]
            print "%s%s\n" % (" " * indentation, sql)
        replace_tuple = (" " * indentation, str(total_time))
        print "%s\033[1;32m[TOTAL TIME: %s seconds]\033[0m" % replace_tuple
        return response


class StaticServeMiddleware(object):
    """
    Middleware to serve media files on developer server
    You must put this at top of all middlewares for speedups
    (Whe dont need sessions, request.user or other stuff)
    """
    MEDIA_URL = getattr(settings, 'MEDIA_URL', None)
    MEDIA_ROOT = getattr(settings, 'MEDIA_ROOT', None)
    IS_ACTIVE = getattr(settings, 'DEBUG', False)

    def process_request(self, request):
        if self.IS_ACTIVE and self.MEDIA_ROOT and self.MEDIA_URL and request.path_info.startswith(self.MEDIA_URL):
            path = request.path_info.replace(self.MEDIA_URL, '').lstrip('/')
            abs_uri = request.build_absolute_uri()
            try:
                response = serve(request, path=path, document_root=self.MEDIA_ROOT)
                print " \033[1;32m[%s] %s\033[0m" % (response.status_code, abs_uri)
                return response
            except Http404:
                print " \033[1;31m[%s] %s\033[0m" % (404, abs_uri)
                raise Http404('Requested file was not found on the file system')
        return None
