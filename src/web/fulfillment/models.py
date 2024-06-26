from django.db import models
from common.models import BaseModel, SingletonModel


class CheckForDefectsType(BaseModel):
    title = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Тип проверки на брак"
        verbose_name_plural = "Типы проверок на брак"


class CheckForDefectsRange(BaseModel):
    defect_type = models.ForeignKey(
        "fulfillment.CheckForDefectsType",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="fulfillment_type_range",
    )
    min_quantity = models.PositiveIntegerField()
    max_quantity = models.PositiveIntegerField()
    price = models.FloatField()

    def __str__(self):
        return f"{self.min_quantity} - {self.max_quantity} шт. по {self.price}"

    class Meta:
        verbose_name = "Проверка на брак"
        verbose_name_plural = "Проверка на брак"



class Acceptance(BaseModel):
    collapse = models.ForeignKey(
        "fulfillment.FulfillmentWorkCollapse",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )
    min_quantity = models.PositiveIntegerField(verbose_name="Минимальное количество")
    max_quantity = models.PositiveIntegerField(verbose_name="Максимальное количество")
    price = models.FloatField(verbose_name="Цена за ФФ", default=0.0)

    def __str__(self):
        return f"{self.min_quantity} - {self.max_quantity} шт. по {self.price}"

    class Meta:
        verbose_name = "Приемка"
        verbose_name_plural = "Приемка"


class Recalculation(BaseModel):
    collapse = models.ForeignKey(
        "fulfillment.FulfillmentWorkCollapse",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )
    min_quantity = models.PositiveIntegerField(verbose_name="Минимальное количество")
    max_quantity = models.PositiveIntegerField(verbose_name="Максимальное количество")
    price = models.FloatField(verbose_name="Цена за ФФ", default=0.0)

    def __str__(self):
        return f"{self.min_quantity} - {self.max_quantity} шт. по {self.price}"

    class Meta:
        verbose_name = "Пересчет"
        verbose_name_plural = "Пересчет"


class Attachment(BaseModel):
    collapse = models.ForeignKey(
        "fulfillment.FulfillmentWorkCollapse",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )
    min_quantity = models.PositiveIntegerField(verbose_name="Минимальное количество")
    max_quantity = models.PositiveIntegerField(verbose_name="Максимальное количество")
    price = models.FloatField(verbose_name="Цена за ФФ", default=0.0)

    def __str__(self):
        return f"{self.min_quantity} - {self.max_quantity} шт. по {self.price}"

    class Meta:
        verbose_name = "Вложение"
        verbose_name_plural = "Вложение"


class MarkingType(BaseModel):
    title = models.CharField(max_length=255, null=False, blank=False)

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
        verbose_name = "Диапозон цен"
        verbose_name_plural = "Диапозон цен"

    def __str__(self):
        return f"{self.min_quantity} - {self.max_quantity} шт. по {self.price}"


class CargoServiceType(models.Model):
    name = models.CharField(max_length=255, unique=False)
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
    price_per_cube = models.CharField(
        verbose_name="Цена за куб", max_length=100, null=False, blank=False
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Упаковка груза"
        verbose_name_plural = "Упаковка груза"


class FulfillmentPackage(BaseModel):
    title = models.CharField(max_length=255, null=False, blank=False)

    class Meta:
        verbose_name = "Упаковка"
        verbose_name_plural = "Упаковка"

    def __str__(self):
        return self.title


class CargoInsurancePrice(BaseModel):
    min_quantity = models.PositiveIntegerField(verbose_name="Минимальная сумма")
    max_quantity = models.PositiveIntegerField(verbose_name="Максимальная сумма")
    price = models.FloatField(verbose_name="Процент от суммы")

    def __str__(self):
        return f"От {self.min_quantity}$/кг до {self.max_quantity}$/кг - {self.price} от суммы"

    class Meta:
        verbose_name = "Страховка"
        verbose_name_plural = "Страховка"


class FulfillmentPackageSize(BaseModel):
    size = models.CharField(
        verbose_name="Размер", max_length=100, null=False, blank=False
    )
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
    collapse = models.ForeignKey(
        "fulfillment.MaterialWorkCollapse",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )
    min_quantity = models.PositiveIntegerField(verbose_name="Минимальное количество")
    max_quantity = models.PositiveIntegerField(verbose_name="Максимальное количество")
    price = models.FloatField(verbose_name="Цена материала")

    class Meta:
        verbose_name = "Бирковние"
        verbose_name_plural = "Бирковние"

    def __str__(self):
        return f"{self.min_quantity} - {self.max_quantity} шт. по {self.price}"


class TagingPriceRangeFF(BaseModel):
    collapse = models.ForeignKey(
        "fulfillment.FulfillmentWorkCollapse",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )
    min_quantity = models.PositiveIntegerField(verbose_name="Минимальное количество")
    max_quantity = models.PositiveIntegerField(verbose_name="Максимальное количество")
    price = models.FloatField(verbose_name="Цена за ФФ", default=0.0)

    class Meta:
        verbose_name = "Биркование"
        verbose_name_plural = "Биркование"

    def __str__(self):
        return f"{self.min_quantity} - {self.max_quantity} Диапазон кол-во"


class BoxPriceRange(BaseModel):
    collapse = models.ForeignKey(
        "fulfillment.MaterialWorkCollapse",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )
    min_quantity = models.PositiveIntegerField(verbose_name="От")
    max_quantity = models.PositiveIntegerField(verbose_name="До")
    price = models.FloatField(verbose_name="Цена")

    class Meta:
        verbose_name = "Короба"
        verbose_name_plural = "Короба"

    def __str__(self):
        return f"{self.min_quantity} - {self.max_quantity} шт. по {self.price}"


class MarkingBoxPriceRangeFF(BaseModel):
    collapse = models.ForeignKey(
        "fulfillment.FulfillmentWorkCollapse",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )
    min_quantity = models.PositiveIntegerField(verbose_name="От")
    max_quantity = models.PositiveIntegerField(verbose_name="До")
    price = models.FloatField(verbose_name="Цена")

    class Meta:
        verbose_name = "Маркировка коробов"
        verbose_name_plural = "Маркировка коробов"

    def __str__(self):
        return f"{self.min_quantity} - {self.max_quantity} шт. по {self.price}"


class LayingBoxPriceRange(BaseModel):
    collapse = models.ForeignKey(
        "fulfillment.FulfillmentWorkCollapse",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )
    min_quantity = models.PositiveIntegerField(verbose_name="От")
    max_quantity = models.PositiveIntegerField(verbose_name="До")
    price = models.FloatField(verbose_name="Цена")

    class Meta:
        verbose_name = "Укладка"
        verbose_name_plural = "Укладка"

    def __str__(self):
        return f"{self.min_quantity} - {self.max_quantity} шт. по {self.price}"


class FulfillmentWorkCollapse(SingletonModel):
    title = models.CharField(verbose_name="Название", max_length=255)

    class Meta:
        verbose_name = "Работа ФФ"
        verbose_name_plural = "Работа ФФ"

    def __str__(self):
        return "Цены за работу ФФ"


class MaterialWorkCollapse(SingletonModel):
    title = models.CharField(verbose_name="Название", max_length=255)

    class Meta:
        verbose_name = "Материалы"
        verbose_name_plural = "Материалы"

    def __str__(self):
        return "Цены на материалы"
