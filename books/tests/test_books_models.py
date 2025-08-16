from books.models import Book
import pytest

pytestmark = pytest.mark.django_db


def test_books_str():
    book = Book.objects.create(
        title="Test Book",
        author="Test Author",
        cover="Soft cover",
        inventory=5,
        daily_fee=12,
    )
    string = str(book)
    assert string == book.title
