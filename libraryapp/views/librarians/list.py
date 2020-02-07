import sqlite3
from django.shortcuts import render
from libraryapp.models import Librarian
from libraryapp.models import model_factory
from ..connection import Connection
from django.contrib.auth.decorators import login_required


@login_required
def list_librarians(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = model_factory(Librarian)
            db_cursor = conn.cursor()

            db_cursor.execute("""
            select
                l.id,
                l.location_id,
                l.user_id,
                u.first_name,
                u.last_name,
                u.email
            from libraryapp_librarian l
            join auth_user u on l.user_id = u.id
            """)

            all_librarians = []
            all_librarians = db_cursor.fetchall()

        template_name = 'librarians/list.html'

        context = {
            'all_librarians': all_librarians
        }

        return render(request, template_name, context)