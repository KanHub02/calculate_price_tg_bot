from rest_framework import serializers

from ..models import Article, RestOther, Scammers


class ArticleListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = ("id", "title")


class ArticleDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = ("description", "link")


class RestOtherSerializer(serializers.ModelSerializer):

    class Meta:
        model = RestOther
        fields = ("id", "title", "file")


class ScammersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scammers
        fields = ("link", )
