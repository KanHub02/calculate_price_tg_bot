from django.contrib import admin

from .models import TelegramClient, LogisticRequest


@admin.register(TelegramClient)
class TelegramClient(admin.ModelAdmin):
    pass


@admin.register(LogisticRequest)
class LogisticRequestAdmin(admin.ModelAdmin):
    pass
