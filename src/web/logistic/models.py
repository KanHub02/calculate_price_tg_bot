from django.db import models
from common.models import BaseModel, SingletonModel


class CargoServiceType(models.Model):
    name = models.CharField(max_length=255, unique=False)
    cargo_type = models.ForeignKey(
        "logistic.CargoType",
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
        "logistic.CargoServiceType",
        on_delete=models.CASCADE,
        related_name="cargo_range",
    )

    def __str__(self):
        return f"{self.min_density} - {self.max_density} Диапазон плотности"


class CargoPackage(BaseModel):
    title = models.CharField(max_length=255, null=False, blank=False)
    price_per_cube = models.CharField(
        verbose_name="Цена за кг", max_length=100, null=False, blank=False
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Упаковка груза"
        verbose_name_plural = "Упаковка груза"


class CargoInsurancePrice(BaseModel):
    min_quantity = models.PositiveIntegerField(verbose_name="Минимальная сумма")
    max_quantity = models.PositiveIntegerField(verbose_name="Максимальная сумма")
    price = models.FloatField(verbose_name="Процент от суммы")

    def __str__(self):
        return f"От {self.min_quantity}$/кг до {self.max_quantity}$/кг - {self.price} от суммы"

    class Meta:
        verbose_name = "Страховка"
        verbose_name_plural = "Страховка"
