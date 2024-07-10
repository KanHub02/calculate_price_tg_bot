from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import CatalogCategory, CatalogProduct, Tag


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
        "tags",
    )
    filter_horizontal = ("tags",)


class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


admin.site.register(CatalogCategory, CatalogCategoryAdmin)
admin.site.register(CatalogProduct, CatalogProductAdmin)
admin.site.register(Tag, TagAdmin)
