from datetime import date

from django.contrib.auth import get_user_model
from django.db import models
from rest_framework.exceptions import ValidationError

from books.models import Book


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='borrowings')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='borrowings')

    def clean(self):
        if self.expected_return_date < date.today():
            raise ValidationError("Expected return date cannot be in the past")
        if self.actual_return_date < self.expected_return_date:
            raise ValidationError("Actual return date cannot be before burrow date")

    def __str__(self):
        return f"{self.book.title} -> {self.user.email}"
