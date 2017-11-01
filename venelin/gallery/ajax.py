import json

from django.http import HttpResponse, HttpResponseBadRequest
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
