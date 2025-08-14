from django.shortcuts import render
from rest_framework import mixins, viewsets

from books.models import Book
from books.serializers import BookSerializer, BookDetailSerializer, BookListSerializer


class BookViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return BookDetailSerializer
        if self.action == 'list':
            return BookListSerializer
        return BookSerializer
