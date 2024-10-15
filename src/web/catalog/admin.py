from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import CatalogCategory, CatalogProduct


class CatalogCategoryAdmin(MPTTModelAdmin):
    list_display = ("title",)
    search_fields = ("title",)


class CatalogProductAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "file",
    )
    search_fields = (
        "title",
        "category__title",
    )
    list_filter = (
        "category",
    )


admin.site.register(CatalogCategory, CatalogCategoryAdmin)
admin.site.register(CatalogProduct, CatalogProductAdmin)
