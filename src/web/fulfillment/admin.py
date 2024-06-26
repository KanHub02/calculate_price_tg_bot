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
    CheckForDefectsRange,
    CheckForDefectsType
)

class CheckForDefectsRangeInline(admin.TabularInline):
    model = CheckForDefectsRange
    fields = ("min_quantity", "max_quantity", "price")


class TagingPriceRangeInline(admin.TabularInline):
    model = TagingPriceRange
    fields = ("min_quantity", "max_quantity", "price")


class BoxPriceRangeInline(admin.TabularInline):
    model = BoxPriceRange
    fields = ("min_quantity", "max_quantity", "price")


class TagingPriceRangeFFInline(admin.TabularInline):
    model = TagingPriceRangeFF
    fields = ("min_quantity", "max_quantity", "price")


class MarkingBoxPriceRangeFFInline(admin.TabularInline):
    model = MarkingBoxPriceRangeFF
    fields = ("min_quantity", "max_quantity", "price")


class AttachmentInline(admin.TabularInline):
    model = Attachment
    fields = ("min_quantity", "max_quantity", "price")


class RecalculationInline(admin.TabularInline):
    model = Recalculation
    fields = ("min_quantity", "max_quantity", "price")


class LayingBoxPriceRangeInline(admin.TabularInline):
    model = LayingBoxPriceRange
    fields = ("min_quantity", "max_quantity", "price")


class AcceptanceInline(admin.TabularInline):
    model = Acceptance
    fields = ("min_quantity", "max_quantity", "price")


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


@admin.register(CheckForDefectsType)
class CheckForDefectsTypeAdmin(admin.ModelAdmin):
    inlines = (CheckForDefectsRangeInline,)
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


@admin.register(MarkingType)
class MarkingTypeAdmin(admin.ModelAdmin):
    inlines = (MarkingTypeRangeInline,)
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


@admin.register(FulfillmentPackage)
class FulfillmentPackageAdmin(admin.ModelAdmin):
    inlines = (FulfillmentPackageSizeInline,)
    fieldsets = (
        (
            "Основное",
            {
                "fields": ("title",),
                "classes": ("wide",),
            },
        ),
    )


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
    fieldsets = (
        (
            "Основное",
            {
                "fields": ("title",),
                "classes": ("wide",),
            },
        ),
    )


@admin.register(MaterialWorkCollapse)
class MaterialWorkCollapseAdmin(admin.ModelAdmin):
    inlines = (
        TagingPriceRangeInline,
        BoxPriceRangeInline,
    )
    fieldsets = (
        (
            "Основное",
            {
                "fields": ("title",),
                "classes": ("wide",),
            },
        ),
    )


@admin.register(CargoInsurancePrice)
class CargoInsurancePriceAdmin(admin.ModelAdmin):
    fields = ("min_quantity", "max_quantity", "price")


@admin.register(CargoPackage)
class CargoPackageAdmin(admin.ModelAdmin):
    fields = ("title", "price_per_cube")
