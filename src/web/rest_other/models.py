from django.db import models

from common.models import BaseModel


class RestOther(BaseModel):
    title = models.CharField(verbose_name="Название", max_length=255, null=False, blank=False)
    file = models.FileField(verbose_name="Файл", null=False, blank=False)


    class Meta:
        verbose_name = "Остальное"
        verbose_name_plural = "Остальное"


# Create your models here.
