from django.contrib import admin

from .models import Article, Scammers, RestOther


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    fields = ("title", "description", "link", "created_at", "updated_at")
    list_display = ("title",)
    list_display_links = ("title",)
    readonly_fields = ("created_at", "updated_at")


@admin.register(Scammers)
class ScammersAdmin(admin.ModelAdmin):
    fields = ("title", "link", "created_at", "updated_at")
    list_display = ("title",)
    list_display_links = ("title",)
    readonly_fields = ("created_at", "updated_at")


@admin.register(RestOther)
class RestOtherAdmin(admin.ModelAdmin):
    list_display = ("title", )
    fields = ("title", "file", "is_deleted", "updated_at", "created_at")
    readonly_fields = ("is_deleted", "updated_at", "created_at")