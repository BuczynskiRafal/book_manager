# book manager app.

The application built in python django allows you to manage a collection of books..

Go to see site online: 
* https://books-manager-rafal-buczynski.herokuapp.com to see book list.
* https://books-manager-rafal-buczynski.herokuapp.com/b/1 to see single book.
* https://books-manager-rafal-buczynski.herokuapp.com/b/add to add new book.
* https://books-manager-rafal-buczynski.herokuapp.com/b/edit/1 to add edit selected book.
* https://books-manager-rafal-buczynski.herokuapp.com/b/delete/1 to add delete selected book.
* https://books-manager-rafal-buczynski.herokuapp.com/b/import to import book from google books. 

See API documentation:
* https://documenter.getpostman.com/view/16990944/UVR5q8gg

## Setup

Requires Python 3

Run these commands:

    git clone https://github.com/BuczynskiRafal/book_manager.git
    py manage.py -m venv venv  
    cd .\venv\Scripts\activate
    pip install -r requirements.txt
    python manage.py migrate
    python manage.py runserver

# Run

    python manage.py runserver

Development Mode
* http://127.0.0.1:8000 to see book list.
* http://127.0.0.1:8000/b/1 to see single book.
* http://127.0.0.1:8000/b/add/ to add new book.
* http://127.0.0.1:8000/b/edit/1 to add edit selected book.
* http://127.0.0.1:8000/b/delete/1 to add delete selected book.
* http://127.0.0.1:8000/b/import  to import book from google books. 
* 
* http://127.0.0.1:8000/api/ to see api view for book list.
* http://127.0.0.1:8000/api/1 to see api view for single book and manage book.
* http://127.0.0.1:8000/api/?search=text to filter and search.
