from django.contrib import admin

from reviews.models import Review


# Register your models here.
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'content', 'rating', 'date_added')
    search_fields =('rating', 'content')
    list_filter = ('book', 'user', 'date_added', 'rating')