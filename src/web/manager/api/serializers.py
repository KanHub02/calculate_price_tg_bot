from rest_framework import serializers

from ..models import Manager, ReviewFormLink, HowToUse, PartnerLead
from common.serializers import MarkdownField


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


class HowToUseSerializer(serializers.ModelSerializer):
    class Meta:
        model = HowToUse
        fields = ("text",)


class PartnerLeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartnerLead
        fields = ("link", )
