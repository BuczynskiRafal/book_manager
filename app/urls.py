from django.urls import path
from .views import all_books
from .views import add_book
from .views import import_from_api
from .views import edit_book
from .views import delete_book
from .views import single_book
from .views import BookList
from .views import BookDetail

urlpatterns = [
    path("b/add", add_book, name="add_book"),
    path("b/import", import_from_api, name="import_book"),
    path("b/edit/<int:id>/", edit_book, name="edit_book"),
    path("b/delete/<int:id>/", delete_book, name="delete_book"),
    path("b/<int:id>/", single_book, name="single_book"),
    path("", all_books, name="list"),
    path('api/', BookList.as_view()),
    path('api/<int:pk>/', BookDetail.as_view()),
]
