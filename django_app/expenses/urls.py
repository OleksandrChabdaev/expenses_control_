from django.urls import path

from .views import (ExpensesListCreateAPIView,
                    ExpensesRetrieveUpdateDestroyAPIView)

app_name = "expenses"
urlpatterns = [
    path("", ExpensesListCreateAPIView.as_view(), name="expenses_list_or_create"),
    path(
        "<int:pk>/",
        ExpensesRetrieveUpdateDestroyAPIView.as_view(),
        name="expenses_detail",
    ),
]
