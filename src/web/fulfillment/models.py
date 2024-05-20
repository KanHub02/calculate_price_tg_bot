from django.db import models
from common.models import BaseModel


class FulfillmentType(BaseModel):
    title = models.CharField(max_length=255, null=False, blank=False)


class FulfillmentTypeRange(BaseModel):
    fulfillment_type = models.ForeignKey(
        "fulfillment.FulfillmentType",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="fulfillment_type_range",
    )
    min_quantity = models.PositiveIntegerField()
    max_quantity = models.PositiveIntegerField()
    price = models.FloatField()


class CargoServiceType(models.Model):
    name = models.CharField(max_length=255, unique=True)
    cargo_type = models.ForeignKey(
        "fulfillment.CargoType",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="cargo_service",
    )
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тип сервиса"
        verbose_name_plural = "Типы сервисов"


class CargoType(BaseModel):
    title = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Тип груза"
        verbose_name_plural = "Типы грузов"



class CargoTypeRange(models.Model):
    min_density = models.FloatField()
    max_density = models.FloatField()
    price = models.FloatField()
    cargo_service = models.ForeignKey(
        "fulfillment.CargoServiceType",
        on_delete=models.CASCADE,
        related_name="cargo_range"
    )

    def __str__(self):
        return f"{self.min_density} - {self.max_density} Density Range"

    class Meta:
        verbose_name = "Диапазон плотности и цены"
        verbose_name_plural = "Диапазоны плотности и цен"


    class Meta:
        verbose_name = "Диапозон цен"
        verbose_name_plural = "Диапозон цен"

class CargoPackage(BaseModel):
    title = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return self.title
    class Meta:
        verbose_name = "Упаковка груза"
        verbose_name_plural = "Упаковка груза"


class FulfillmentPackage(BaseModel):
    title = models.CharField(max_length=255, null=False, blank=False)
