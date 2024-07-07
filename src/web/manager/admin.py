from django.contrib import admin

from .models import Manager, FeedbackLink


@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ("tg_username", "tg_id", "phone_number")
    fields = ("tg_username", "tg_id", "phone_number", "created_at", "updated_at")
    readonly_fields = ("phone_number", "created_at", "updated_at")


@admin.register(FeedbackLink)
class FeedbackLinkAdmin(admin.ModelAdmin):
    list_display = ("title","link",)
    fields = ("title", "link", "created_at", "updated_at")
    readonly_fields = ("created_at", "updated_at")