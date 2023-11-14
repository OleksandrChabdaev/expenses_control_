from django.db import IntegrityError
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Item
from .serializers import ItemSerializer


class ItemListCreateAPIView(ListCreateAPIView):
    """
    Get list of all "Items" created by user or create new "Item" for user.
    Accepts GET, POST methods.
    Display fields: "id", "name", "user".
    Returns: list of Item model fields.
    """

    permission_classes = (IsAuthenticated,)
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    pagination_class = None

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if (
            int(serializer.initial_data["user"]) != self.request.user.id
            and not self.request.user.is_superuser
            or self.request.user.is_staff
        ):
            return Response(status=status.HTTP_403_FORBIDDEN)
        try:
            self.perform_create(serializer)
        except IntegrityError:
            content = {
                "error": f"Item name {serializer.initial_data['name']} already exists for user id {serializer.initial_data['user']}."
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
