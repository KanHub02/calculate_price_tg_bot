from django.contrib import admin

from .models import MarkingPrice, DoubleMarkingPrice, StandardPackingPrice, AssemblyPrice, TaggingPrice, InsertsPrice, StackingPrice
from common.admin import SingletonModelAdmin


@admin.register(MarkingPrice)
class MarkingPriceAdmin(SingletonModelAdmin):
    list_display = ['min_quantity', 'max_quantity', 'price']

@admin.register(DoubleMarkingPrice)
class DoubleMarkingPriceAdmin(SingletonModelAdmin):
    list_display = ['min_quantity', 'max_quantity', 'price']

@admin.register(StandardPackingPrice)
class StandardPackingPriceAdmin(SingletonModelAdmin):
    list_display = ['min_quantity', 'max_quantity', 'price']

@admin.register(AssemblyPrice)
class AssemblyPriceAdmin(SingletonModelAdmin):
    list_display = ['min_quantity', 'max_quantity', 'price']

@admin.register(TaggingPrice)
class TaggingPriceAdmin(SingletonModelAdmin):
    list_display = ['min_quantity', 'max_quantity', 'price']

@admin.register(InsertsPrice)
class InsertsPriceAdmin(SingletonModelAdmin):
    list_display = ['min_quantity', 'max_quantity', 'price']

@admin.register(StackingPrice)
class StackingPriceAdmin(SingletonModelAdmin):
    list_display = ['min_quantity', 'max_quantity', 'price']
