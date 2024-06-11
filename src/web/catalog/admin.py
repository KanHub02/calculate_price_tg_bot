from django.contrib import admin

from .models import CatalogCategory, CatalogProduct


@admin.register(CatalogCategory)
class CatalogCategoryAdmin(admin.ModelAdmin):
    list_display = ("title",)
    fields = ("title", "is_deleted", "created_at", "updated_at")
    readonly_fields = ("created_at", "updated_at")


@admin.register(CatalogProduct)
class CatalogProductAdmin(admin.ModelAdmin):
    list_display = ("title", "category")
    fields = ("title", "category", "file", "is_deleted", "created_at", "updated_at")
    readonly_fields = ("created_at", "updated_at")
