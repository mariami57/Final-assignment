from django import forms

from books.models import Book
from destinations.models import Destination



class BookDestinationHandlerMixin:
    def handle_book_and_destination(self, form):
        instance = form.instance
        is_edit = form.instance.pk is not None

        new_book = False
        new_dest = False

        book_choice = form.cleaned_data.get('book_choice')
        book_title = form.cleaned_data.get('book_title')

        dest_choice = form.cleaned_data.get('destination_choice')
        d_name = form.cleaned_data.get('destination_name')
        d_country = form.cleaned_data.get('destination_country')
        lat = form.cleaned_data.get('latitude')
        lng = form.cleaned_data.get('longitude')

        if book_choice == 'other' and book_title:
            book = Book.objects.create(
                title=book_title, author="Unknown", added_by=self.request.user,
            )
            new_book = True
        elif book_choice:
            book = Book.objects.get(id=book_choice)
        else:
            book = None


        if dest_choice == 'other' and d_name and d_country:

            destination = Destination.objects.create(
                name=d_name,
                country=d_country,
                latitude= lat,
                longitude= lng
            )
            new_dest = True
        elif dest_choice:
            destination = Destination.objects.get(id=dest_choice)
        else:
            destination = None

        if is_edit and book and destination:
            book.destinations.set([destination])
        elif book and destination:
            if (new_book or new_dest) and destination not in book.destinations.all():
                book.destinations.add(destination)

        return book, destination