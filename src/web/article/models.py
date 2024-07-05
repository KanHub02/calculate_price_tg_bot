from django.db import models

from common.models import BaseModel


class Article(BaseModel):
    title = models.CharField(verbose_name="Название", max_length=255, null=False, blank=False)
    description = models.TextField(verbose_name="Описание", null=False, blank=False)
    photo = models.ImageField(verbose_name="Фото", null=True, blank=True)

    class Meta:
        verbose_name = "Полезная статья"
        verbose_name_plural = "Полезные статьи"


# Create your models here.
