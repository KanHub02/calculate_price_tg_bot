from django.db import models

from common.models import BaseModel, SingletonModel


class Article(BaseModel):
    title = models.CharField(
        verbose_name="Название", max_length=255, null=False, blank=False
    )
    description = models.TextField(verbose_name="Описание", null=False, blank=False)
    link = models.URLField(verbose_name="Ссылка на статью", null=False, blank=False)

    class Meta:
        verbose_name = "Полезная статья"
        verbose_name_plural = "Полезные статьи"


class Scammers(SingletonModel):
    link = models.URLField(verbose_name="Ссылка на статью", null=False, blank=False)

    class Meta:
        verbose_name = "Статья про мошенников"
        verbose_name_plural = "Статья про мошенников"


class RestOther(BaseModel):
    title = models.CharField(
        verbose_name="Название", max_length=255, null=False, blank=False
    )
    file = models.FileField(verbose_name="Файл", null=False, blank=False)

    class Meta:
        verbose_name = "Остальное"
        verbose_name_plural = "Остальное"


# Create your models here.
