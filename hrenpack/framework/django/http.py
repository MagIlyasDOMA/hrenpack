"""
Django HTTP response utilities.

Provides extended JsonResponse class with data property and JSON extraction.

Утилиты HTTP ответов Django.

Предоставляет расширенный класс JsonResponse со свойством data и извлечение JSON.
"""

import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse as DjangoJsonResponse
from hrenpack.typings import JsonData


def extract_json_response(response: DjangoJsonResponse):
    """
    Extract JSON data from Django JsonResponse.

    Извлекает JSON данные из Django JsonResponse.

    Args:
        response (DjangoJsonResponse): JsonResponse object / Объект JsonResponse

    Returns:
        dict: Parsed JSON data / Разобранные JSON данные
    """
    return json.loads(response.content.decode(response.charset))


class JsonResponse(DjangoJsonResponse):
    """
    Extended JsonResponse with non-ASCII characters preserved and data property.

    Расширенный JsonResponse с сохранением не-ASCII символов и свойством data.

    Args:
        data: Data to serialize / Данные для сериализации
        encoder: JSON encoder class / Класс JSON энкодера
        safe: Safe mode / Безопасный режим
        json_dumps_params: Parameters for json.dumps / Параметры для json.dumps
        **kwargs: Additional arguments for parent class / Дополнительные аргументы
    """

    def __init__(self, data, encoder=DjangoJSONEncoder, safe: bool = True, json_dumps_params=None, **kwargs):
        kwargs.setdefault('json_dumps_params', {})
        kwargs['json_dumps_params'].setdefault('ensure_ascii', False)
        super().__init__(data, **kwargs)

    @property
    def data(self) -> JsonData:
        """
        Get parsed JSON data from response.

        Получает разобранные JSON данные из ответа.

        Returns:
            JsonData: Parsed JSON data / Разобранные JSON данные
        """
        return extract_json_response(self)
