from django.contrib import admin

from .models import TransitPrice, Stock


class TransitPriceInline(admin.TabularInline):
    model = TransitPrice
    fields = ("quantity", "price")


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    fields = ("title", "created_at")
    list_display = ("title", )
    readonly_fields = ("created_at", )
    inlines = (TransitPriceInline, )