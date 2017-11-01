from django.core.exceptions import MiddlewareNotUsed
from django.utils.deprecation import MiddlewareMixin
from django.utils.encoding import DjangoUnicodeDecodeError
from django.utils.html import strip_spaces_between_tags as minify_html
from django.conf import settings
from django.db import connection


class SQLPrintingMiddleware(MiddlewareMixin):
    """
    Middleware which prints out a list of all SQL queries done
    for each view that is processed. This is only useful for debugging.
    """
    def __init__(self, *args, **kwargs):
        if not settings.DEBUG:
            raise MiddlewareNotUsed
        super().__init__(*args, **kwargs)

    def process_response(self, request, response):
        if (len(connection.queries) == 0 or
                request.path_info.startswith('/favicon.ico') or
                request.path_info.startswith(settings.STATIC_URL) or
                request.path_info.startswith(settings.MEDIA_URL)):
            return response

        indentation = 2
        print("\n\n%s\033[1;35m[SQL Queries for]\033[1;34m %s\033[0m\n" % (" " * indentation, request.path_info))
        total_time = 0.0
        for query in connection.queries:
            nice_sql = query['sql'].replace('"', '').replace(',', ', ')
            sql = "\033[1;31m[%s]\033[0m %s" % (query['time'], nice_sql)
            total_time += float(query['time'])
            print("%s%s\n" % (" " * indentation, sql))
        replace_tuple = (" " * indentation, str(total_time))
        print("%s\033[1;32m[TOTAL TIME: %s seconds]\033[0m" % replace_tuple)
        return response


class XUACompatibleMiddleware(MiddlewareMixin):
    """
    Add a X-UA-Compatible header to the response
    This header tells to Internet Explorer to render page with latest
    possible version or to use chrome frame if it is installed.
    """
    def process_response(self, request, response):
        response['X-UA-Compatible'] = 'IE=edge,chrome=1'
        return response


class MinifyHTMLMiddleware(MiddlewareMixin):
    """
    Remove spaces between html tags

    Taken from django-pipeline but but modified to not be executed in debug.
    """
    def __init__(self, *args, **kwargs):
        if settings.DEBUG:
            raise MiddlewareNotUsed
        super().__init__(*args, **kwargs)

    def process_response(self, request, response):
        if response.has_header('Content-Type') and 'text/html' in response['Content-Type']:
            try:
                response.content = minify_html(response.content.strip())
            except DjangoUnicodeDecodeError:
                pass
        return response
