from django.contrib import admin


class SingletonModelAdmin(admin.ModelAdmin):
    pass
    # def has_add_permission(self, request):
    #     # Disable add permission for singleton models
    #     return False
    #
    # def has_delete_permission(self, request, obj=None):
    #     # Disable delete permission for singleton models
    #     return False
    #
    # def change_view(self, request, object_id, form_url='', extra_context=None):
    #     if not self.model.objects.exists():
    #         # If no instance exists, create one
    #         self.model.load()
    #     return super().change_view(request, object_id, form_url, extra_context)
    #
    # def changelist_view(self, request, extra_context=None):
    #     # Redirect to change view if the model is singleton
    #     obj = self.model.load()
    #     return self.change_view(request, str(obj.pk), extra_context)
