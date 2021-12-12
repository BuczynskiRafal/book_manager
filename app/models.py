from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=256, blank=False)
    authors = models.CharField(max_length=256, blank=False)
    published_date = models.CharField(max_length=20, default=1900)
    isbn_10 = models.CharField(max_length=256, null=True, blank=True)
    isbn_13 = models.CharField(max_length=256, null=True, blank=True)
    page_count = models.IntegerField(default=0, null=True, blank=True)
    image_links = models.CharField(max_length=1024, null=True, blank=True)
    language = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return f"Title: {self.title} Author: {self.authors}"
