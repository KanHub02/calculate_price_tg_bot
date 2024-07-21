from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin


from .models import BeforeCource, AfterCourse, TranslateCryptiInfo, TranslateRfInfo


@admin.register(BeforeCource)
class BeforeCourceAdmin(admin.ModelAdmin):
    pass


@admin.register(AfterCourse)
class AfterCourseAdmin(admin.ModelAdmin):
    pass


@admin.register(TranslateCryptiInfo)
class TranslateCryptiInfoAdmin(admin.ModelAdmin):
    fields = ("text", )


@admin.register(TranslateRfInfo)
class TranslateRfInfoAdmin(admin.ModelAdmin):
    fields = ("text", )

