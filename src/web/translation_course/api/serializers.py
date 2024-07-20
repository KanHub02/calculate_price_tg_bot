from rest_framework import serializers

from ..models import BeforeCource, AfterCourse, TranslateCryptiInfo, TranslateRfInfo


class TranslateCryptiInfoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TranslateCryptiInfo
        fields = ("text", )


class TranslateRfInfoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TranslateRfInfo
        fields = ("text", )


class BeforeCourceSerializer(serializers.ModelSerializer):

    class Meta:
        model = BeforeCource
        fields = (
            "rub_yuan",
            "som_yuan",
            "updated_at",
        )


class AfterCourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = AfterCourse
        fields = (
            "rub_yuan",
            "som_yuan",
            "updated_at",
        )
