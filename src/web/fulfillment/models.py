from django.db import models
from common.models import BaseModel


class Acceptance(BaseModel):
    ff_per_price = models.FloatField(verbose_name="Цена за ФФ", default=0.0)

    def __str__(self):
        return f"Цена за приемку: {self.ff_per_price}"




class MarkingType(BaseModel):
    title = models.CharField(max_length=255, null=False, blank=False)
    ff_per_price = models.FloatField(verbose_name="Цена за ФФ", default=0.0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Тип маркировки"
        verbose_name_plural = "Типы маркировок"


class MarkingTypeRange(BaseModel):
    fulfillment_type = models.ForeignKey(
        "fulfillment.MarkingType",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="fulfillment_type_range",
    )
    min_quantity = models.PositiveIntegerField()
    max_quantity = models.PositiveIntegerField()
    price = models.FloatField()

    class Meta:
        verbose_name = "Диапазон цен"
        verbose_name_plural = "Диапазоны цен"


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
        related_name="cargo_range",
    )

    def __str__(self):
        return f"{self.min_density} - {self.max_density} Диапазон плотности"

    class Meta:
        verbose_name = "Диапазон плотности и цены"
        verbose_name_plural = "Диапазоны плотности и цен"


class CargoPackage(BaseModel):
    title = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Упаковка груза"
        verbose_name_plural = "Упаковка груза"


class FulfillmentPackage(BaseModel):
    title = models.CharField(max_length=255, null=False, blank=False)
    ff_per_price = models.FloatField(verbose_name="Цена за ФФ", default=0.0)

    class Meta:
        verbose_name = "Упаковка"
        verbose_name_plural = "Упаковка"

    def __str__(self):
        return self.title


class FulfillmentPackageSize(BaseModel):
    size = models.CharField(
        verbose_name="Размер", max_length=100, null=False, blank=False
    )
    ff_per_price = models.FloatField(verbose_name="Цена за ФФ", default=0.0)
    price = models.FloatField(verbose_name="Цена материалы", null=False, blank=False)
    package = models.ForeignKey(
        "fulfillment.FulfillmentPackage",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="fulfillment_package_size",
    )

    class Meta:
        verbose_name = "Размеры"
        verbose_name_plural = "Размеры"


class TagingPriceRange(BaseModel):
    min_quantity = models.PositiveIntegerField(verbose_name="Минимальное количество")
    max_quantity = models.PositiveIntegerField(verbose_name="Максимальное количество")
    price = models.FloatField(verbose_name="Цена материала")
    ff_per_price = models.FloatField(verbose_name="Цена за ФФ", default=0.0)

    class Meta:
        verbose_name = "Диапазон цен на маркировку"
        verbose_name_plural = "Диапазоны цен на маркировку"

    def __str__(self):
        return f"{self.min_quantity} - {self.max_quantity} шт. по {self.price}"

class TagingPriceRangeFF(BaseModel):
    ff_per_price = models.FloatField(verbose_name="Цена за ФФ", default=0.0)

    class Meta:
        verbose_name = "Работа фф за единицу маркировки"
        verbose_name_plural = "Работа фф за единицу маркировки"

    def __str__(self):
        return f"{self.min_quantity} - {self.max_quantity} шт. по {self.price} руб."


class BoxPriceRange(BaseModel):
    min_quantity = models.PositiveIntegerField(verbose_name="От")
    max_quantity = models.PositiveIntegerField(verbose_name="До")
    price = models.FloatField(verbose_name="Цена")

    class Meta:
        verbose_name = "Диапазон цен на коробки"
        verbose_name_plural = "Диапазоны цен на коробки"

    def __str__(self):
        return f"{self.min_quantity} - {self.max_quantity} шт. по {self.price}"


class MarkingBoxPriceRange(BaseModel):
    min_quantity = models.PositiveIntegerField(verbose_name="От")
    max_quantity = models.PositiveIntegerField(verbose_name="До")
    price = models.FloatField(verbose_name="Цена материала")

    class Meta:
        verbose_name = "Диапазон цен на маркированные коробки"
        verbose_name_plural = "Диапазоны цен на маркированные коробки"

    def __str__(self):
        return f"{self.min_quantity} - {self.max_quantity} шт. по {self.price}"


class LayingBoxPriceRange(BaseModel):
    min_quantity = models.PositiveIntegerField(verbose_name="От")
    max_quantity = models.PositiveIntegerField(verbose_name="До")
    price = models.FloatField(verbose_name="Цена")
    ff_per_price = models.FloatField(verbose_name="Цена за ФФ", default=0.0)

    class Meta:
        verbose_name = "Диапазон цен на укладки в коробы"
        verbose_name_plural = "Диапазоны цен на укладку в короб"

    def __str__(self):
        return f"{self.min_quantity} - {self.max_quantity} шт. по {self.price}"

