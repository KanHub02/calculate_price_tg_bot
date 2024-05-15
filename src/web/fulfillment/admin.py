from django.contrib import admin

from .models import (
    FulfillmentType,
    FulfillmentTypeRange,
    CargoType, 
    CargoTypeRange,
    )



class FulfillmentTypeRangeInline(admin.TabularInline):
    fields = ("min_quantity", "max_quantity", "price")
    max_num = 5
    model = FulfillmentTypeRange


class CargoTypeRangeInline(admin.TabularInline):
    fields = ("min_quantity", "max_quantity", "price")
    max_num = 5
    model = CargoTypeRange


@admin.register(FulfillmentType)
class FulfillmentTypeAdmin(admin.ModelAdmin):
    inlines = (FulfillmentTypeRangeInline, )
    fields = ("id", "title", "created_at", "updated_at", "is_deleted")
    readonly_fields = ("id", "created_at", "updated_at")
    list_display = ("title",)


@admin.register(CargoType)
class CargoTypeAdmin(admin.ModelAdmin):
    inlines = (CargoTypeRangeInline, )
    fields = ("id", "title", "created_at", "updated_at", "is_deleted")
    readonly_fields = ("id", "created_at", "updated_at")
    list_display = ("title",)

