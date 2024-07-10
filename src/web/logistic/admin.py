from django.contrib import admin

from .models import (
    CargoType,
    CargoTypeRange,
    CargoPackage,
    CargoServiceType,
    CargoInsurancePrice,
)


class CargoServiceTypeInline(admin.TabularInline):
    fields = ("name",)
    model = CargoServiceType


class CargoTypeRangeInline(admin.TabularInline):
    model = CargoTypeRange
    fields = ("min_density", "max_density", "price")


class CargoServiceInline(admin.TabularInline):
    fieldsets = (
        (
            "Диапозон цен",
            {
                "fields": ("cargo_type_range",),
                "classes": ("wide",),
            },
        ),
    )
    max_num = 5
    model = CargoServiceType


@admin.register(CargoServiceType)
class CargoServiceTypeAdmin(admin.ModelAdmin):
    inlines = (CargoTypeRangeInline,)
    list_display = ("get_correct_name",)
    fieldsets = (
        (
            "Основное",
            {
                "fields": ("name", "cargo_type"),
                "classes": ("wide",),
            },
        ),
    )

    def get_correct_name(self, obj):
        return f"{obj.name} - {obj.cargo_type.title}"

    get_correct_name.short_description = "Тип доставки"


@admin.register(CargoType)
class CargoTypeAdmin(admin.ModelAdmin):
    # inlines = (CargoServiceInline,)
    fieldsets = (
        (
            "Основное",
            {
                "fields": ("title",),
                "classes": ("wide",),
            },
        ),
    )
    readonly_fields = ("id", "created_at", "updated_at")
    list_display = ("title",)


@admin.register(CargoInsurancePrice)
class CargoInsurancePriceAdmin(admin.ModelAdmin):
    fields = ("min_quantity", "max_quantity", "price")


@admin.register(CargoPackage)
class CargoPackageAdmin(admin.ModelAdmin):
    fields = ("title", "price_per_cube")
