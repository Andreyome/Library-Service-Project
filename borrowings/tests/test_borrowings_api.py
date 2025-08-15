from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from books.models import Book
from borrowings.models import Borrowing

BORROWINGS_URL = reverse("borrowings:borrowing-list")


def sample_book(**params):
    defaults = {
        "title": "test",
        "author": "test",
        "cover": "SOFT",
        "inventory": 2,
        "daily_fee": 12,
    }
    defaults.update(params)
    return Book.objects.create(**defaults)


class UnauthenticatedBorrowingsAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        response = self.client.get(BORROWINGS_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AuthenticatedNonAdminBorrowingsAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass",
        )
        self.client.force_authenticate(self.user)

    def test_create_borrowing(self):
        book = sample_book()
        payload = {
            "expected_return_date": date.today(),
            "book": 1,
        }
        response = self.client.post(BORROWINGS_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AuthenticatedAdminBorrowingsAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass",
            is_staff=True,
        )
        self.client.force_authenticate(self.user)

    def test_create_borrowing(self):
        book = sample_book()
        payload = {
            "expected_return_date": date.today(),
            "book": 1,
        }
        response = self.client.post(BORROWINGS_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        borrowing = Borrowing.objects.get(pk=response.data["id"])
        self.assertEqual(borrowing.book, book)
        self.assertEqual(
            borrowing.expected_return_date, payload["expected_return_date"]
        )
        self.assertEqual(borrowing.borrow_date, date.today())
