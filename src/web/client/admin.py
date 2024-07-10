from django.contrib import admin

from .models import (
    TelegramClient,
    LogisticRequest,
    CargoServicePrice,
    FulFillmentRequest,
    FeedbackForUseful,
)


class LogisticRequestInline(admin.TabularInline):
    model = LogisticRequest
    fieldsets = (
        (
            "Основное",
            {
                "fields": (
                    "telegram_client",
                    "cargo_type",
                    "cargo_package_type",
                    "weight",
                    "volume",
                    "density",
                    "price_before_insurance",
                    "insurance_cost",
                    "created_at",
                ),
                "classes": "wide",
            },
        ),
    )
    readonly_fields = ("created_at",)


class FulFillmentRequestInline(admin.TabularInline):
    model = FulFillmentRequest
    fieldsets = (
        (
            "Основное",
            {
                "fields": ("product_title", "quantity", "telegram_client"),
                "classes": "wide",
            },
        ),
        (
            "Фулфилмент",
            {
                "fields": (
                    "marking_type",
                    "package",
                    "need_attachment",
                    "need_taging",
                    "ff_total_price",
                    "per_price_ff",
                ),
                "classes": "wide",
            },
        ),
        (
            "Материалы",
            {
                "fields": (
                    "packaging_size",
                    "count_of_boxes",
                    "material_total_price",
                    "need_check_defects",
                    "per_price_material",
                ),
                "classes": "wide",
            },
        ),
        (
            "Транзит",
            {
                "fields": ("transit", "per_price_transit"),
                "classes": "wide",
            },
        ),
    )


class CargoServicePriceInline(admin.TabularInline):
    max_num = 5
    min_num = 1
    model = CargoServicePrice
    fields = ("cargo_service", "price")


@admin.register(TelegramClient)
class TelegramClient(admin.ModelAdmin):
    list_display = ("tg_username", "tg_id")
    fieldsets = (
        (
            "Основное",
            {
                "fields": (
                    "tg_username",
                    "tg_id",
                    "phone_number",
                    "tg_bio",
                    "created_at",
                ),
                "classes": "wide",
            },
        ),
    )
    readonly_fields = ("created_at", "is_deleted")
    inlines = (LogisticRequestInline, FulFillmentRequestInline)


@admin.register(LogisticRequest)
class LogisticRequestAdmin(admin.ModelAdmin):
    list_display = ("telegram_client", "cargo_type", "created_at")
    list_display_links = ("telegram_client", "cargo_type", "created_at")
    fieldsets = (
        (
            "Основное",
            {
                "fields": (
                    "telegram_client",
                    "cargo_type",
                    "cargo_package_type",
                    "weight",
                    "volume",
                    "density",
                    "price_before_insurance",
                    "insurance_cost",
                    "created_at",
                ),
                "classes": "wide",
            },
        ),
    )
    readonly_fields = ("created_at",)
    inlines = (CargoServicePriceInline,)


@admin.register(FulFillmentRequest)
class FulFillmentRequestAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "Основное",
            {
                "fields": ("product_title", "quantity", "telegram_client"),
                "classes": "wide",
            },
        ),
        (
            "Фулфилмент",
            {
                "fields": (
                    "need_check_defects",
                    "marking_type",
                    "package",
                    "need_attachment",
                    "need_taging",
                    "ff_total_price",
                    "per_price_ff",
                ),
                "classes": "wide",
            },
        ),
        (
            "Материалы",
            {
                "fields": (
                    "packaging_size",
                    "count_of_boxes",
                    "material_total_price",
                    "per_price_material",
                ),
                "classes": "wide",
            },
        ),
        (
            "Транзит",
            {
                "fields": ("transit", "per_price_transit"),
                "classes": "wide",
            },
        ),
    )


@admin.register(FeedbackForUseful)
class FeedbackForUsefulAdmin(admin.ModelAdmin):
    fields = ("telegram_client", "feedback", "created_at")
    readonly_fields = ("telegram_client", "feedback", "created_at")
