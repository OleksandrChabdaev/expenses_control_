from rest_framework import serializers

from .models import Expenses
from item.models import Item


class ExpensesSerializer(serializers.ModelSerializer):
    item = serializers.CharField(source="item.name")

    class Meta:
        model = Expenses
        fields = ["id", "user", "date", "time", "item", "cost"]

    def create(self, validated_data):
        item, created = Item.objects.get_or_create(
            name=validated_data["item"]["name"], user=validated_data["user"]
        )
        if created:
            print(f"{item} was created.")
        validated_data["item"] = item
        return super().create(validated_data)

    def update(self, instance, validated_data):
        item, created = Item.objects.get_or_create(
            name=validated_data["item"]["name"], user=validated_data["user"]
        )
        if created:
            print(f"{item} was created.")
        validated_data["item"] = item
        return super().update(instance, validated_data)
