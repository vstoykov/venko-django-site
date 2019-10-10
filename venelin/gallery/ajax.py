import json
from functools import wraps

from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder


JSON_CONTENT_TYPE = 'application/json; charset=%s' % (settings.DEFAULT_CHARSET, )


class JSONResponseMixin(object):
    """
    Response that will return JSON serialized value of the content.

    """
    INDENT = 1 if settings.DEBUG else None

    def __init__(self, content, *args, **kwargs):
        json_content = json.dumps(content, cls=DjangoJSONEncoder, indent=self.INDENT)
        super().__init__(json_content, JSON_CONTENT_TYPE, *args, **kwargs)


class JSONResponse(JSONResponseMixin, HttpResponse):
    pass


class JSONResponseBadRequest(JSONResponseMixin, HttpResponseBadRequest):
    pass


def json_view(fn):
    @wraps(fn)
    def wrapper(request, *args, **kwargs):
        try:
            response = fn(request, *args, **kwargs)
        except Http404 as e:
            response = JSONResponse(
                {
                    'errors': [{
                        'code': 'NOT FOUND',
                        'description': str(e),
                    }]
                },
                status=404,
            )
        if isinstance(response, HttpResponse):
            return response
        return JSONResponse(response)
    return wrapper
