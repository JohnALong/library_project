import sqlite3
from django.shortcuts import render, redirect, reverse
from libraryapp.models import Library
from libraryapp.models import model_factory
from libraryapp.models import Book
from ..connection import Connection
from django.contrib.auth.decorators import login_required


def create_library(cursor, row):
    _row = sqlite3.Row(cursor, row)

    library = Library()
    library.id = _row["id"]
    library.title = _row["title"]
    library.address = _row["address"]

    # Note: You are adding a blank books list to the library object
    # This list will be populated later (see below)

    library.books = []

    book = Book()
    book.id = _row["book_id"]
    book.title = _row["book_title"]
    book.author = _row["author"]
    book.ISBN_number = _row["ISBN_number"]
    book.year_published = _row["year_published"]

    # Return a tuple containing the library and the
    # book built from the data in the current row of
    # the data set
    return (library, book,)

@login_required
def list_libraries(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = create_library
            db_cursor = conn.cursor()

            db_cursor.execute("""
            SELECT
                l.id,
                l.title,
                l.address,
                b.id book_id,
                b.title book_title,
                b.author,
                b.year_published,
                b.ISBN_number
            FROM libraryapp_library l
            JOIN libraryapp_book b ON l.id = b.location_id
            """)
            #returns a list of tuples with all the data
            all_libraries = db_cursor.fetchall()
            #starting with empty dictionary to change tuple into usable data
            library_groups = {}
            #iterate the tuples
            for (library, book) in all_libraries:

                # if dictionary doesn't have a key of current library id value, add the key and set the value to the current library
                if library.id not in library_groups:
                    library_groups[library.id] = library
                    library_groups[library.id].books.append(book)

                # if the key exists, append current book to list of books for current library
                else:
                    library_groups[library.id].books.append(book)


        template_name = 'libraries/list.html'

        context = {
            'all_libraries': library_groups.values()
        }

        return render(request, template_name, context)

    elif request.method == 'POST':
        form_data = request.POST

        with sqlite3.connect(Connection.db_path) as conn:
            db_cursor = conn.cursor()

            db_cursor.execute("""
            INSERT INTO libraryapp_library
            (
                title, address
            )
            VALUES (?, ?)
            """,
            (form_data['title'], form_data['address']))

        return redirect(reverse('libraryapp:libraries'))