from django.contrib import admin

from .models import (
    TelegramClient,
    LogisticRequest,
    CargoServicePrice,
    FulFillmentRequest,
)


class LogisticRequestInline(admin.TabularInline):
    max_num = 5
    min_num = 1
    model = LogisticRequest
    fields = (
        "cargo_type",
        "cargo_package_type",
        "weight",
        "quantity",
        "insurance_cost",
    )


class CargoServicePriceInline(admin.TabularInline):
    max_num = 5
    min_num = 1
    model = CargoServicePrice
    fields = ("cargo_service", "price")


@admin.register(TelegramClient)
class TelegramClient(admin.ModelAdmin):
    list_display = ("tg_username", "tg_id")

    fields = (
        "tg_username",
        "tg_id",
        "phone_number",
        "tg_bio",
        "created_at",
        "is_deleted",
    )
    readonly_fields = ("created_at", "is_deleted")
    inlines = (LogisticRequestInline,)


@admin.register(LogisticRequest)
class LogisticRequestAdmin(admin.ModelAdmin):
    list_display = ("telegram_client", "cargo_type", "created_at")
    list_display_links = ("telegram_client", "cargo_type", "created_at")
    fields = (
        "telegram_client",
        "cargo_type",
        "cargo_package_type",
        "weight",
        "volume",
        "density",
        "cube",
        "price_before_insurance",
        "insurance_cost",
        "created_at",
    )
    readonly_fields = ("created_at",)
    inlines = (CargoServicePriceInline,)


@admin.register(FulFillmentRequest)
class FulFillmentRequestAdmin(admin.ModelAdmin):
    pass
