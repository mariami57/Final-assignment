from django.contrib import admin

from destinations.models import Destination


# Register your models here.
@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'created_by')
    list_filter = ('country',)
    search_fields = ('name',)
    exclude = ('created_by',)
    readonly_fields = ('created_by',)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.added_by = request.user
        super().save_model(request, obj, form, change)