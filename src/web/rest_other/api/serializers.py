from rest_framework import serializers

from ..models import RestOther


class RestOtherSerializer(serializers.ModelSerializer):

    class Meta:
        model = RestOther
        fields = ("id","title", "file")