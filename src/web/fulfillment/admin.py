from django.contrib import admin

from .models import (
    MarkingType,
    MarkingTypeRange,
    CargoType,
    CargoTypeRange,
    CargoPackage,
    CargoServiceType,
    FulfillmentPackage,
    FulfillmentPackageSize,
    TagingPriceRange,
    BoxPriceRange,
    MarkingBoxPriceRangeFF,
    FulfillmentWorkCollapse,
    MaterialWorkCollapse,
    Attachment,
    Recalculation,
    LayingBoxPriceRange,
    TagingPriceRangeFF,
    Acceptance,
    CargoInsurancePrice,
)


class TagingPriceRangeInline(admin.TabularInline):
    model = TagingPriceRange


class BoxPriceRangeInline(admin.TabularInline):
    model = BoxPriceRange


class TagingPriceRangeFFInline(admin.TabularInline):
    model = TagingPriceRangeFF


class MarkingBoxPriceRangeFFInline(admin.TabularInline):
    model = MarkingBoxPriceRangeFF


class AttachmentInline(admin.TabularInline):
    model = Attachment


class RecalculationInline(admin.TabularInline):
    model = Recalculation


class LayingBoxPriceRangeInline(admin.TabularInline):
    model = LayingBoxPriceRange


class AcceptanceInline(admin.TabularInline):
    model = Acceptance


class FulfillmentPackageSizeInline(admin.TabularInline):
    fields = ("size", "price")
    model = FulfillmentPackageSize


class MarkingTypeRangeInline(admin.TabularInline):
    fields = ("min_quantity", "max_quantity", "price")
    max_num = 5
    model = MarkingTypeRange


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
    fields = ("name", "cargo_type")

    def get_correct_name(self, obj):
        return f"{obj.name} - {obj.cargo_type.title}"

    get_correct_name.short_description = "Тип доставки"


@admin.register(MarkingType)
class MarkingTypeAdmin(admin.ModelAdmin):
    inlines = (MarkingTypeRangeInline,)
    fields = ("title", "created_at", "is_deleted")
    readonly_fields = ("id", "created_at", "updated_at")
    list_display = ("title",)


@admin.register(CargoType)
class CargoTypeAdmin(admin.ModelAdmin):
    # inlines = (CargoServiceInline,)
    fields = ("id", "title", "created_at", "updated_at", "is_deleted")
    readonly_fields = ("id", "created_at", "updated_at")
    list_display = ("title",)


@admin.register(FulfillmentPackage)
class FulfillmentPackageAdmin(admin.ModelAdmin):
    inlines = (FulfillmentPackageSizeInline,)


@admin.register(FulfillmentWorkCollapse)
class FulfillmentWorkCollapseAdmin(admin.ModelAdmin):
    inlines = (
        TagingPriceRangeFFInline,
        MarkingBoxPriceRangeFFInline,
        AttachmentInline,
        RecalculationInline,
        LayingBoxPriceRangeInline,
        AcceptanceInline,
    )


@admin.register(MaterialWorkCollapse)
class MaterialWorkCollapseAdmin(admin.ModelAdmin):
    inlines = (
        TagingPriceRangeInline,
        BoxPriceRangeInline,
    )


@admin.register(CargoInsurancePrice)
class CargoInsurancePriceAdmin(admin.ModelAdmin):
    fileds = ("min_quantity", "max_quantity", "price")


@admin.register(CargoPackage)
class CargoPackageAdmin(admin.ModelAdmin):
    fields = ("title", "price_per_cube")
