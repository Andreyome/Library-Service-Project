from datetime import date

from django.core.exceptions import ValidationError
from rest_framework import serializers

from books.serializers import BookDetailSerializer
from borrowings.models import Borrowing


class BorrowingSerializer(serializers.ModelSerializer):
    book = BookDetailSerializer(read_only=True)
    class Meta:
        model = Borrowing
        fields = ["id", "borrow_date", "expected_return_date", "actual_return_date", "book", "user"]


class BorrowingDetailSerializer(serializers.ModelSerializer):
    book = BookDetailSerializer(read_only=True)
    class Meta:
        model = Borrowing
        fields = ["id", "borrow_date", "expected_return_date", "actual_return_date", "book", "user"]


class BorrowingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ["expected_return_date","book", "user"]

    def validate(self, data):
        book = data["book"]
        if book.inventory == 0:
            raise ValidationError("Book out of stock")
        if data["expected_return_date"] < date.today:
            raise ValidationError("Expected return date cannot be in the past")
        return data

    def create(self, validated_data):
        book = validated_data["book"]
        book.inventory -= 1
        book.save()
        return super().create(validated_data)

