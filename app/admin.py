from django.contrib import admin
from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "authors",
        "published_date",
        "isbn_10",
        "isbn_13",
        "page_count",
        "image_links",
        "language",
    ]
