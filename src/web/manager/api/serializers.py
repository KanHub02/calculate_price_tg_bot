from rest_framework import serializers

from ..models import Manager


class ManagerListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Manager
        fields = ("full_name", "tg_id", "tg_username", "phone_number")
