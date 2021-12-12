import requests
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import filters
from .forms import BooksForm
from .models import Book
from .serializers import BooksSerializer


class BookList(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BooksSerializer
    filter_backends = [filters.SearchFilter]
    filter_fields = {
        'title': ['exact'],
        'authors': ['exact'],
        'language': ['exact'],
        'published_date': ['gte', 'lte', 'exact', 'gt', 'lt'],
    }
    search_fields = ['title', 'authors', 'language', 'published_date']


class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BooksSerializer


def valid(param):
    return param != "" and param is not None


def all_books(request):
    queryset = Book.objects.all()
    title = request.GET.get("title")
    author = request.GET.get("author")
    language = request.GET.get("language")
    start = request.GET.get("start")
    end = request.GET.get("end")

    if valid(title):
        queryset = Book.objects.filter(title__icontains=title)
    if valid(author):
        queryset = Book.objects.filter(authors__icontains=author)
    if valid(language):
        queryset = Book.objects.filter(language__icontains=language)
    if valid(start):
        queryset = Book.objects.filter(published_date__gte=start)
    if valid(end):
        queryset = Book.objects.filter(published_date__lte=end)
    return render(request, "book/list.html", {"queryset": queryset})


def single_book(request, id):
    book = get_object_or_404(Book, pk=id)
    return render(request, "book/book.html", {"book": book})


def add_book(request):
    if request.method == "POST":
        book_form = BooksForm(request.POST or None)
        if book_form.is_valid():
            book = book_form.save()
            return redirect(all_books)

        return render(
            request,
            "book/add_book.html",
            {"book_form": book_form, "new": True},
        )
    else:
        book_form = BooksForm()
    return render(
        request,
        "book/add_book.html",
        {"book_form": book_form, "new": True},
    )


def edit_book(request, id):
    book = get_object_or_404(Book, pk=id)

    book_form = BooksForm(request.POST or None, request.FILES or None, instance=book)

    if book_form.is_valid():
        book = book_form.save()
        return redirect(all_books)
    return render(request, "book/add_book.html", {"book_form": book_form})


def delete_book(request, id):
    book = get_object_or_404(Book, pk=id)

    if request.method == "POST":
        book.delete()
        return redirect(all_books)
    return render(request, "book/confirm.html", {"book": book})


def import_from_api(request):
    books = []
    count = 0
    query = request.GET.get("title")

    if valid(query):
        url = "https://www.googleapis.com/books/v1/volumes?q={}&printType=books"
        url = url.format(query)
        r = requests.get(url)
        results = r.json()["items"]
        for result in results:
            try:
                isbn_10 = list(
                    filter(
                        lambda i: i["type"] == "ISBN_10",
                        result["volumeInfo"]["industryIdentifiers"],
                    )
                )[0]["identifier"]
                isbn_13 = list(
                    filter(
                        lambda i: i["type"] == "ISBN_13",
                        result["volumeInfo"]["industryIdentifiers"],
                    )
                )[0]["identifier"]
            except IndexError:
                isbn_10 = 'Not assigned'
                isbn_13 = 'Not assigned'
            except KeyError:
                pass

            try:
                book = {
                    "title": result["volumeInfo"]["title"],
                    "authors": result["volumeInfo"]["authors"][0],
                    "published_date": result["volumeInfo"]["publishedDate"],
                    "isbn_10": isbn_10,
                    "isbn_13": isbn_13,
                    "page_count": result["volumeInfo"]["pageCount"],
                    "image_links": result["volumeInfo"]["imageLinks"]["thumbnail"],
                    "language": result["volumeInfo"]["language"],
                }
                books.append(book)
                count += 1
            except KeyError:
                pass
    if request.method == "POST":
        number = request.POST.get("number")
        try:
            form = BooksForm(books[int(number) - 1])
            if form.is_valid():
                book_item = form.save(commit=False)
                book_item.save()
                count = "imported book nr:" + number
        except IndexError:
            count = "wrong index number"
    return render(
        request, "book/book_import.html", {"books": books, "count": count}
    )
