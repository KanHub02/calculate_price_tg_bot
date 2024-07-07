from django.contrib import admin

from .models import (
    MarkingType,
    MarkingTypeRange,
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
