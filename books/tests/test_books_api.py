from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from books.models import Book

BOOKS_URL = reverse("books:book-list")


class UnauthenticatedBooksAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        response = self.client.get(BOOKS_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AuthenticatedNonAdminBooksAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass",
        )
        self.client.force_authenticate(self.user)

    def test_create_book(self):
        payload = {
            "title": "test",
            "author": "test",
            "cover": "SOFT",
            "inventory": 2,
            "daily_fee": 12,
        }
        response = self.client.post(BOOKS_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AuthenticatedAdminBooksAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass",
            is_staff=True,
        )
        self.client.force_authenticate(self.user)

    def test_create_book(self):
        payload = {
            "title": "test",
            "author": "test",
            "cover": "SOFT",
            "inventory": 2,
            "daily_fee": 12,
        }
        response = self.client.post(BOOKS_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        book = Book.objects.get(pk=response.data["id"])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(book, key))
