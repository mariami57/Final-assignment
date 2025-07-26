from django.contrib import admin

from books.models import Book


# Register your models here.
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    exclude = ('added_by',)
    readonly_fields = ('added_by',)
    list_display = ('title', 'author', 'genre', 'added_by')
    list_filter = ('destinations', 'added_by', 'author')
    search_fields = ('title', 'author', 'genre')

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.added_by = request.user
        super().save_model(request, obj, form, change)
