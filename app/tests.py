from django.test import Client
from django.test import TestCase
from django.urls import reverse
from django.urls import resolve

from .views import *
from .models import Book
from .forms import BooksForm


class UrlsTests(TestCase):

    # urls
    def test_url_add_new_book(self):
        url = reverse("add_book")
        self.assertEquals(resolve(url).func, add_book)

    def test_url_import_book_form_google_api(self):
        url = reverse("import_book")
        self.assertEquals(resolve(url).func, import_from_api)

    def test_url_edit_book(self):
        url = reverse("edit_book", kwargs={"id": 1})
        self.assertEquals(resolve(url).func, edit_book)

    def test_url_delete_book(self):
        url = reverse("delete_book", kwargs={"id": 1})
        self.assertEquals(resolve(url).func, delete_book)

    def test_url_show_single_book(self):
        url = reverse("single_book", kwargs={"id": 1})
        self.assertEquals(resolve(url).func, single_book)

    def test_url_show_all_book_list(self):
        url = reverse("list")
        self.assertEquals(resolve(url).func, all_books)


class ViewsTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.book = Book.objects.create(
            title="test_title",
            authors="test_authors",
            published_date="1900",
            isbn_10="12345",
            isbn_13="56789",
            page_count="324",
            image_links="http://books.google.com/books/content?id=cs5MDwAAQBAJ&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api",
            language="en",
        )

    def tearDown(self):
        del self.client
        del self.book

    def test_view_add_new_book(self):
        response = self.client.get(reverse("add_book"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "book/add_book.html")

    def test_view_import_book_form_google_api(self):
        response = self.client.get(reverse("import_book"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "book/book_import.html")

    def test_view_edit_book(self):
        response = self.client.get(reverse("edit_book", kwargs={"id": 1}))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "book/add_book.html")

    def test_view_delete_book(self):
        response = self.client.get(reverse("delete_book", kwargs={"id": 1}))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "book/confirm.html")

    def test_view_show_single_book(self):
        response = self.client.get(reverse("single_book", kwargs={"id": 1}))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "book/book.html")

    def test_view_show_all_book_list(self):
        response = self.client.get(reverse("list"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "book/list.html")


class ModelTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.book = Book.objects.create(
            title="test_title",
            authors="test_authors",
            published_date="1900",
            isbn_10="12345",
            isbn_13="56789",
            page_count="324",
            image_links="http://books.google.com/books/content?id=cs5MDwAAQBAJ&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api",
            language="en",
        )

    def tearDown(self):
        del self.client
        del self.book

    def test_book_as_text(self):
        self.assertEqual(
            str(self.book),
            f"Title: {self.book.title} Author: {self.book.authors}",
        )

    def test_book_title_is_not_empty(self):
        self.assertNotEqual(self.book.title, None)

    def test_book_author_is_not_empty(self):
        self.assertNotEqual(self.book.authors, None)


class FormTests(TestCase):
    def setUp(self):
        self.form = BooksForm(
            data={
                "title": "test_title",
                "authors": "test_authors",
                "published_date": "1900",
                "isbn_10": "12345",
                "isbn_13": "56789",
                "page_count": "324",
                "image_links": "http://books.google.com/books/content?id=cs5MDwAAQBAJ&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api",
                "language": "en",
            }
        )

    def tearDown(self):
        del self.form

    def test_book_form_is_valid(self):
        self.assertTrue(self.form.is_valid())
