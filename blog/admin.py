from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("name", "is_published", "date_posted")
    list_filter = ("date_posted",)
    search_fields = ("name", "content")
