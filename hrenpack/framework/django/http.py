import json
from django.http import JsonResponse as DjangoJsonResponse
from hrenpack.typings import JsonData


def extract_json_response(response: DjangoJsonResponse):
    return json.loads(response.content.decode(response.charset))


class JsonResponse(DjangoJsonResponse):
    @property
    def data(self) -> JsonData:
        return extract_json_response(self)
