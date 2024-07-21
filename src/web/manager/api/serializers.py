from rest_framework import serializers

from ..models import Manager, ReviewFormLink


class ManagerListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Manager
        fields = ("full_name", "tg_id", "tg_username", "phone_number")


class GetManagerChatIDSerializer(serializers.ModelSerializer):

    class Meta:
        model = Manager
        fields = ("tg_id",)


class ReviewFormLinkSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReviewFormLink
        fields = ("link", )