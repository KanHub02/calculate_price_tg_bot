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
    CheckForDefectsType,
    HonestSign,
    MaterialWorkingPriceRange
)


class MaterialWorkingPriceRangeInline(admin.TabularInline):
    model = MaterialWorkingPriceRange
    fields = ("min_quantity", "max_quantity", "price")
    ordering = ("min_quantity", )


class HonestSignInline(admin.TabularInline):
    model = HonestSign
    fields = ("min_quantity", "max_quantity", "price")
    ordering = ("min_quantity", )


class CheckForDefectsRangeInline(admin.TabularInline):
    model = CheckForDefectsRange
    fields = ("min_quantity", "max_quantity", "price")
    ordering = ("min_quantity", )


class TagingPriceRangeInline(admin.TabularInline):
    model = TagingPriceRange
    fields = ("min_quantity", "max_quantity", "price")
    ordering = ("min_quantity", )


class BoxPriceRangeInline(admin.TabularInline):
    model = BoxPriceRange
    fields = ("min_quantity", "max_quantity", "price")
    ordering = ("min_quantity", )


class TagingPriceRangeFFInline(admin.TabularInline):
    model = TagingPriceRangeFF
    fields = ("min_quantity", "max_quantity", "price")
    ordering = ("min_quantity", )


class MarkingBoxPriceRangeFFInline(admin.TabularInline):
    model = MarkingBoxPriceRangeFF
    fields = ("min_quantity", "max_quantity", "price")
    ordering = ("min_quantity", )


class AttachmentInline(admin.TabularInline):
    model = Attachment
    fields = ("min_quantity", "max_quantity", "price")
    ordering = ("min_quantity", )


class RecalculationInline(admin.TabularInline):
    model = Recalculation
    fields = ("min_quantity", "max_quantity", "price")
    ordering = ("min_quantity", )


class LayingBoxPriceRangeInline(admin.TabularInline):
    model = LayingBoxPriceRange
    fields = ("min_quantity", "max_quantity", "price")
    ordering = ("min_quantity", )


class AcceptanceInline(admin.TabularInline):
    model = Acceptance
    fields = ("min_quantity", "max_quantity", "price")
    ordering = ("min_quantity", )


class FulfillmentPackageSizeInline(admin.TabularInline):
    fields = ("size", "price")
    model = FulfillmentPackageSize
    ordering = ("price", )


class MarkingTypeRangeInline(admin.TabularInline):
    fields = ("min_quantity", "max_quantity", "price")
    max_num = 5
    model = MarkingTypeRange
    ordering = ("min_quantity", )


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
        # TagingPriceRangeFFInline,
        MarkingBoxPriceRangeFFInline,
        AttachmentInline,
        RecalculationInline,
        # LayingBoxPriceRangeInline,
        AcceptanceInline,
        HonestSignInline,
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
        MaterialWorkingPriceRangeInline,
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
