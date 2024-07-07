from django.db import models

from common.models import BaseModel


class Article(BaseModel):
    title = models.CharField(verbose_name="Название", max_length=255, null=False, blank=False)
    description = models.TextField(verbose_name="Описание", null=False, blank=False)
    link = models.URLField(verbose_name="Ссылка на статью", null=False, blank=False)


    class Meta:
        verbose_name = "Полезная статья"
        verbose_name_plural = "Полезные статьи"


# Create your models here.
