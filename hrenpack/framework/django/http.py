import json

from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse as DjangoJsonResponse
from hrenpack.typings import JsonData


def extract_json_response(response: DjangoJsonResponse):
    return json.loads(response.content.decode(response.charset))


class JsonResponse(DjangoJsonResponse):
    def __init__(self, data, encoder=DjangoJSONEncoder, safe: bool = True, json_dumps_params=None, **kwargs):
        kwargs.setdefault('json_dumps_params', {})
        kwargs['json_dumps_params'].setdefault('ensure_ascii', False)
        super().__init__(data, **kwargs)

    @property
    def data(self) -> JsonData:
        return extract_json_response(self)
