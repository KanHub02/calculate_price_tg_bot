from django.contrib import admin

from .models import (
    FulfillmentType,
    FulfillmentTypeRange,
    CargoType,
    CargoTypeRange,
    CargoPackage,
    CargoServiceType,
)


class FulfillmentTypeRangeInline(admin.TabularInline):
    fields = ("min_quantity", "max_quantity", "price")
    max_num = 5
    model = FulfillmentTypeRange

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


@admin.register(CargoPackage)
class CargoPackageAdmin(admin.ModelAdmin):
    pass

@admin.register(CargoServiceType)
class CargoServiceTypeAdmin(admin.ModelAdmin):
    inlines = (CargoTypeRangeInline, )
    list_display = ("get_correct_name",)
    fields = ("name", "cargo_type")

    def get_correct_name(self, obj):
        return f'{obj.name} - {obj.cargo_type.title}'

    get_correct_name.short_description = "Тип доставки"

@admin.register(FulfillmentType)
class FulfillmentTypeAdmin(admin.ModelAdmin):
    inlines = (FulfillmentTypeRangeInline,)
    fields = ("id", "title", "created_at", "updated_at", "is_deleted")
    readonly_fields = ("id", "created_at", "updated_at")
    list_display = ("title",)


@admin.register(CargoType)
class CargoTypeAdmin(admin.ModelAdmin):
    # inlines = (CargoServiceInline,)
    fields = ("id", "title", "created_at", "updated_at", "is_deleted")
    readonly_fields = ("id", "created_at", "updated_at")
    list_display = ("title",)
