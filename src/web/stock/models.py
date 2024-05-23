from django.db import models

from common.models import BaseModel


class Stock(BaseModel):
    title = models.CharField(verbose_name="Название", max_length=250)
    location = models.CharField(verbose_name="Локация", max_length=250)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Склад"
        verbose_name_plural = "Склады"


class TransitPrice(BaseModel):
    stock = models.ForeignKey(
        "stock.Stock",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        verbose_name="Склад",
        related_name="transit_price",
    )
    quantity = models.FloatField(verbose_name="Кол-во коробок")
    price = models.FloatField(verbose_name="Цена")

    class Meta:
        verbose_name = "Цена"
        verbose_name_plural = "Цены"
