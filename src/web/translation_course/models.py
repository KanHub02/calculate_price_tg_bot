from django.db import models

from common.models import SingletonModel


class BeforeCource(SingletonModel):
    rub_yuan = models.CharField(verbose_name="Рубль - Юань", max_length=255)
    som_yuan = models.CharField(verbose_name="Сом - Юань", max_length=255)
    
    class Meta:
        verbose_name = "До 100’000 юаней"
        verbose_name_plural = "До 100’000 юаней"

    def __str__(self) -> str:
        return f"{self.rub_yuan}: {self.som_yuan}"


class AfterCourse(SingletonModel):
    rub_yuan = models.CharField(verbose_name="Рубль - Юань", max_length=255)
    som_yuan = models.CharField(verbose_name="Сом - Юань", max_length=255)
    
    class Meta:
        verbose_name = "Свыше 100’000 юаней "
        verbose_name_plural = "Свыше 100’000 юаней"

    def __str__(self) -> str:
        return f"{self.rub_yuan}: {self.som_yuan}"