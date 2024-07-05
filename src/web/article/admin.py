from django.contrib import admin

from .models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    fields = ("title", "description", "photo", "created_at", "updated_at")
    list_display = ("title",)
    list_display_links = ("title",)
    readonly_fields = ("created_at", "updated_at")
