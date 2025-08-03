from django.contrib import admin

from posts.models import Post


# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'book', 'destination', 'content', 'user', 'created_at')
    search_fields = ('title', 'content')
    list_filter = ('created_at', 'destination', 'book', 'user')