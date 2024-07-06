from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.core.exceptions import ValidationError
from common.models import BaseModel

class Tag(BaseModel):
    name = models.CharField(
        verbose_name="Тег", max_length=100, null=False, blank=False
    )

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self) -> str:
        return self.name

class CatalogCategory(MPTTModel, BaseModel):
    title = models.CharField(
        verbose_name="Название", max_length=255, null=False, blank=False
    )
    parent = TreeForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='children'
    )

    class MPTTMeta:
        order_insertion_by = ['title']

    class Meta:
        verbose_name = "Категория товара"
        verbose_name_plural = "Категории товаров"

    def __str__(self) -> str:
        return self.title

class CatalogProduct(BaseModel):
    category = TreeForeignKey(
        "catalog.CatalogCategory",
        verbose_name="Категория",
        on_delete=models.CASCADE,
        related_name="products",
    )
    title = models.CharField(
        verbose_name="Название", max_length=255, null=False, blank=False
    )
    file = models.FileField(verbose_name="PDF")
    tags = models.ManyToManyField(Tag, verbose_name="Теги", related_name="products", blank=True)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self) -> str:
        return self.title

    def clean(self):
        if self.category and not self.category.is_leaf_node():
            raise ValidationError('Продукт может быть присвоен только подкатегории.')