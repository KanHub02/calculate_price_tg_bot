from django.contrib import admin

from .models import CatalogCategory, CatalogProduct


@admin.register(CatalogCategory)
class CatalogCategoryAdmin(admin.ModelAdmin):
    list_display = ("title",)
    fields = ("title",)


@admin.register(CatalogProduct)
class CatalogProductAdmin(admin.ModelAdmin):
    list_display = ("title", "category")
    fields = ("title", "category", "file")
