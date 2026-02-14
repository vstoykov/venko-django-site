from django.http.request import HttpRequest
from django.http.response import JsonResponse
from django.utils.encoding import force_str


def whoami(request: HttpRequest):
    meta_name = lambda m: m[5:].replace('_', '-').title() if m.startswith('HTTP_') else m
    return JsonResponse(
        {
            meta_name(meta): force_str(value)
            for (meta, value) in request.META.items()
            if not (meta.startswith('wsgi') or meta.startswith('uwsgi'))
        }
    )
