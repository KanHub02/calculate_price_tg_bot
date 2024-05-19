from typing import Dict, Union
from django.db.models import QuerySet


from ..models import TelegramClient


class TelegramClientService(object):

    _model = TelegramClient

    @classmethod
    def get_or_create(
        cls, validated_data: Dict
    ) -> Union[QuerySet[TelegramClient], None]:
        return cls._model.objects.get_or_create(**validated_data)
