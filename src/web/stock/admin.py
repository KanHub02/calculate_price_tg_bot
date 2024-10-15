from django.contrib import admin

from .models import TransitPrice, Stock


class TransitPriceInline(admin.TabularInline):
    model = TransitPrice
    fields = ("quantity", "price")
    ordering = ("quantity", )


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ("title",)
    readonly_fields = ("created_at",)
    inlines = (TransitPriceInline,)
    fieldsets = (
        (
            "Основное",
            {
                "fields": ("title",),
                "classes": "wide",
            },
        ),
    )
