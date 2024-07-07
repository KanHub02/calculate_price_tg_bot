from rest_framework import serializers

from ..models import Article


class ArticleListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = ("id", "title")


class ArticleDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = ("description", "link")
