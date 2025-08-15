from datetime import date

from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
    extend_schema_view,
)
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from books.permissions import IsAdminOrReadOnly
from borrowings.models import Borrowing
from borrowings.serializers import (
    BorrowingSerializer,
    BorrowingDetailSerializer,
    BorrowingCreateSerializer,
    BorrowingReturnSerializer,
)


@extend_schema_view(
    list=extend_schema(
        summary="List borrowings",
        responses=BorrowingSerializer,
    ),
    retrieve=extend_schema(
        summary="Retrieve borrowing details",
        responses=BorrowingDetailSerializer,
    ),
    create=extend_schema(
        summary="Create a borrowing (inventory decreases by 1)",
        request=BorrowingCreateSerializer,
        responses=BorrowingDetailSerializer,
    ),
)
class BorrowingViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Borrowing.objects.select_related("user", "book")
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action == "list":
            return BorrowingSerializer
        if self.action == "retrieve":
            return BorrowingDetailSerializer
        if self.action == "create":
            return BorrowingCreateSerializer
        if self.action == "return_book":
            return BorrowingReturnSerializer
        return BorrowingSerializer

    @extend_schema(
        summary="Return a borrowed book (inventory increases by 1)",
        description="Sets `actual_return_date` to today. Available only to the borrowing owner or admin.",
        responses={200: OpenApiResponse(description="Book successfully returned")},
    )
    @action(detail=True, methods=["post"], url_path="return")
    def return_book(self, request, pk=None):
        borrowing = self.get_object()
        if borrowing.actual_return_date:
            return Response(
                {"detail": "Book already returned."}, status=status.HTTP_400_BAD_REQUEST
            )

        borrowing.actual_return_date = date.today()
        borrowing.book.inventory += 1
        borrowing.book.save()
        borrowing.save()
        return Response({"detail": "Book returned successfully."})
