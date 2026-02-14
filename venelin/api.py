import re
from django.http.request import HttpRequest
from django.http.response import JsonResponse
from django.utils.encoding import force_str


def whoami(request: HttpRequest):
    meta_name = lambda m: m[5:].replace('_', '-').title() if m.startswith('HTTP_') else m
    hidden_meta_re = re.compile(r'^(wsgi|uwsgi|HTTP_COOKIE|CSRF_COOKIE)')
    data = {
        meta_name(meta): force_str(value)
        for (meta, value) in request.META.items()
        if not hidden_meta_re.match(meta)
    }
    return JsonResponse(data)
