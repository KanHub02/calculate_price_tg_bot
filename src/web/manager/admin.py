from django.contrib import admin
from django.db import models
from django_summernote.admin import SummernoteModelAdmin
from django_summernote.utils import get_attachment_model
from .models import Manager, FeedbackLink, HowToUse, WorkingConditions, ReviewFormLink, PartnerLead

admin.site.unregister(get_attachment_model())


@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ("tg_username", "tg_id", "phone_number")
    fields = ("tg_username", "tg_id", "phone_number", "created_at", "updated_at")
    readonly_fields = ("phone_number", "created_at", "updated_at")


@admin.register(FeedbackLink)
class FeedbackLinkAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "link",
    )
    fields = ("title", "link", "created_at", "updated_at")
    readonly_fields = ("created_at", "updated_at")


@admin.register(HowToUse)
class HowToUseAdmin(admin.ModelAdmin):
    fields = ("text",)

@admin.register(WorkingConditions)
class WorkingConditionsAdmin(admin.ModelAdmin):
    fields = ("text",)


@admin.register(PartnerLead)
class PartnerLeadAdmin(admin.ModelAdmin):
    fields = ("link", )

@admin.register(ReviewFormLink)
class ReviewFormLinkAdmin(admin.ModelAdmin):
    fields = ("link", )
