from django.contrib import admin
from .models import RestOther


@admin.register(RestOther)
class RestOtherAdmin(admin.ModelAdmin):
    list_display = ("title", )
    fields = ("title", "file", "is_deleted", "updated_at", "created_at")
    readonly_fields = ("is_deleted", "updated_at", "created_at")
# Register your models here.
