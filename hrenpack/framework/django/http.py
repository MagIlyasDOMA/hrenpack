import json
from django.http import JsonResponse as DjangoJsonResponse


def extract_json_response(response: DjangoJsonResponse):
    return json.loads(response.content.decode(response.charset))


class JsonResponse(DjangoJsonResponse):
    @property
    def data(self):
        return extract_json_response(self)
