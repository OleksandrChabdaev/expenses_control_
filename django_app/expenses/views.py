from django.db.models import Sum
from django_filters import rest_framework as filters
from rest_framework import status
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from user.permissions import IsOwnerPermission

from .models import Expenses
from .serializers import ExpensesSerializer


class ExpensesFilter(filters.FilterSet):
    item = filters.CharFilter(field_name="item__name", lookup_expr="exact")
    date_from = filters.DateFilter(field_name="date", lookup_expr="gte")
    date_to = filters.DateFilter(field_name="date", lookup_expr="lte")
    time_from = filters.TimeFilter(field_name="time", lookup_expr="gte")
    time_to = filters.TimeFilter(field_name="time", lookup_expr="lte")

    class Meta:
        model = Expenses
        fields = ["item", "date", "time"]


class ExpensesListCreateAPIView(ListCreateAPIView):
    """
    Get list of all "Expenses" created by user or create new "Expenses" for user.
    Accepts GET, POST methods.
    Display fields: "id", "user", "date", "time", "item", "cost".
    Returns: list of Expenses model fields.
    """

    permission_classes = (IsAuthenticated,)
    queryset = Expenses.objects.all()
    serializer_class = ExpensesSerializer
    pagination_class = None
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ExpensesFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        expenses_dict = {}
        for expense in serializer.data:
            date = str(expense.get("date"))
            if date not in expenses_dict.keys():
                expenses_dict[date] = []
            expenses_dict[date].append(expense)
        for date in expenses_dict.keys():
            day_limit = self.request.user.day_sum
            day_sum = 0
            for expenses in expenses_dict[date]:
                day_sum += expenses.get("cost")
                if day_sum <= day_limit:
                    expenses["over_day_limit"] = True
                else:
                    expenses["over_day_limit"] = False
        return Response(expenses_dict)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if (
            int(serializer.initial_data["user"]) != self.request.user.id
            and not self.request.user.is_superuser
            or self.request.user.is_staff
        ):
            return Response(status=status.HTTP_403_FORBIDDEN)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class ExpensesRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """
    Reads, updates and deletes Expenses model fields.
    Accepts GET, PATCH, DELETE methods.
    Accepted field: "id".
    Display fields: "id", "user", "date", "time", "item", "cost".
    Returns: Expenses model fields.
    """

    permission_classes = (IsAuthenticated, IsOwnerPermission)
    queryset = Expenses.objects.all()
    serializer_class = ExpensesSerializer
    http_method_names = ("get", "patch", "delete")
    lookup_url_kwarg = "pk"

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        if (
            int(request.data["user"]) != self.request.user.id
            and not self.request.user.is_superuser
            or self.request.user.is_staff
        ):
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# class ListModelMixin:
#     def list(self, request, *args, **kwargs):
#         queryset = self.filter_queryset(self.get_queryset())
#         page = self.paginate_queryset(queryset)
#         if page is not None:
#             serializer = self.get_serializer(page, many=True)
#             return self.get_paginated_response(serializer.data)
#         serializer = self.get_serializer(queryset, many=True)
#         return Response(serializer.data)
