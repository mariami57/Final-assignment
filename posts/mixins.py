from books.models import Book
from destinations.models import Destination
from posts.models import Post


class BookDestinationHandlerMixin:
    def handle_book_and_destination(self, form):
        instance = form.instance
        is_edit = form.instance.pk is not None

        new_book = False
        new_dest = False

        book_choice = form.cleaned_data.get('book_choice')
        book_title = form.cleaned_data.get('book_title')

        dest_choice = form.cleaned_data.get('destination_choice')
        dest_name = form.cleaned_data.get('destination_name')

        if book_choice == 'other' and book_title:
            book = Book.objects.create(
                title=book_title,author="Unknown", added_by=self.request.user,)
            new_book = True
        else:
            book = Book.objects.get(id=book_choice)

        if dest_choice == 'other' and dest_name:
            d_name, d_country = dest_name.split(',')
            destination = Destination.objects.create(
                name=d_name,
                country=d_country,
                )
            new_dest = True
        else:
            destination = Destination.objects.get(id=dest_choice)

        if is_edit:
            book.destinations.set([destination])

        else:
            if (new_book or new_dest) and destination not in book.destinations.all():
                book.destinations.add(destination)

        return book, destination