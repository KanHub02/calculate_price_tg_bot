from django.contrib import admin


from .models import BeforeCource, AfterCourse


@admin.register(BeforeCource)
class BeforeCourceAdmin(admin.ModelAdmin):
    pass


@admin.register(AfterCourse)
class AfterCourseAdmin(admin.ModelAdmin):
    pass
# Register your models here.
