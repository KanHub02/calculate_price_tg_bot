from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from django_summernote.utils import get_attachment_model  

from .models import Manager, FeedbackLink, HowToUse, WorkingConditions

admin.site.unregister(get_attachment_model())

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


@admin.register(HowToUse)
class HowToUseAdmin(SummernoteModelAdmin):
    fields = ("text", )
    summernote_fields = ("text", )


@admin.register(WorkingConditions)
class WorkingConditionsAdmin(SummernoteModelAdmin):
    fields = ("text", )
    summernote_fields = ("text", )
