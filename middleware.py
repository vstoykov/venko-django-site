import os

from django.views.static import serve, Http404
from django.core.exceptions import MiddlewareNotUsed
from django.utils.encoding import DjangoUnicodeDecodeError
from django.utils.html import strip_spaces_between_tags as minify_html
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
    def __init__(self):
        if not settings.DEBUG:
            raise MiddlewareNotUsed

    def process_response(self, request, response):
        if (len(connection.queries) == 0 or
            request.path_info.startswith('/favicon.ico') or
            request.path_info.startswith(settings.STATIC_URL) or
            request.path_info.startswith(settings.MEDIA_URL)):
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


class XUACompatibleMiddleware(object):
    """
    Add a X-UA-Compatible header to the response
    This header tells to Internet Explorer to render page with latest
    possible version or to use chrome frame if it is installed.
    """
    def process_response(self, request, response):
        response['X-UA-Compatible'] = 'IE=edge,chrome=1'
        return response


class MinifyHTMLMiddleware(object):
    """
    Remove spaces between html tags

    Taken from django-pipeline but but modified to not be executed in debug.
    """
    def __init__(self):
        if settings.DEBUG:
            raise MiddlewareNotUsed

    def process_response(self, request, response):
        if response.has_header('Content-Type') and 'text/html' in response['Content-Type']:
            try:
                response.content = minify_html(response.content.strip())
            except DjangoUnicodeDecodeError:
                pass
        return response
