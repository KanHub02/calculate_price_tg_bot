from rest_framework import serializers

from ..models import BeforeCource, AfterCourse


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
