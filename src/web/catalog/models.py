from django.db import models

from common.models import BaseModel


class CatalogCategory(BaseModel):
    title = models.CharField(
        verbose_name="Название", max_length=255, null=False, blank=False
    )

    class Meta:
        verbose_name = "Категория товара"
        verbose_name_plural = "Категории товаров"

    def __str__(self) -> str:
        return self.title


class CatalogProduct(BaseModel):
    category = models.ForeignKey(
        "catalog.CatalogCategory",
        verbose_name="Категория",
        on_delete=models.CASCADE,
        related_name="product",
    )
    title = models.CharField(
        verbose_name="Название", max_length=255, null=False, blank=False
    )
    file = models.FileField(verbose_name="PDF")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self) -> str:
        return self.title
