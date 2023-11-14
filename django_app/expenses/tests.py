import json
import logging

from django.urls import reverse
from rest_framework import status
from user.tests import UserBase

from .models import Expenses
from .serializers import ExpensesSerializer

logger = logging.getLogger("root")


class ExpensesTestCase(UserBase):
    fixtures = [
        "user/fixtures/user_fixtures.json",
        "item/fixtures/item_fixtures.json",
        "expenses/fixtures/expenses_fixtures.json",
    ]

    def setUp(self):
        super().setUp()
        self.data_create = {
            "cost": 10,
            "item": "watermelon",
            "user": 1003,
            "date": "2023-03-05",
            "time": "00:00",
        }

        self.data_patch = {
            "cost": 10,
            "item": "peach",
            "user": 1003,
            "date": "2023-03-05",
            "time": "00:00",
        }

    def test_create_expenses_as_not_auth_user(self):
        url = reverse("expenses:expenses_list_or_create")
        self.client.force_authenticate(user=None)
        response = self.client.post(url, self.data_create)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_expenses_by_not_owner(self):
        url = reverse("expenses:expenses_list_or_create")
        self.client.force_authenticate(user=self.ex_4_user)
        response = self.client.post(url, self.data_create)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_expenses_by_owner(self):
        url = reverse("expenses:expenses_list_or_create")
        self.client.force_authenticate(user=self.ex_3_user)
        response = self.client.post(url, self.data_create)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_expenses_as_not_auth_user(self):
        self.client.force_authenticate(user=None)
        response = self.get_item(1001)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_expenses_by_owner(self):
        self.client.force_authenticate(user=self.ex_3_user)
        response = self.get_item(1005)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_expenses_by_not_owner(self):
        self.client.force_authenticate(user=self.ex_4_user)
        response = self.get_item(1006)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def get_item(self, id):
        url = reverse("expenses:expenses_detail", kwargs={"pk": id})
        return self.client.get(url)

    def test_patch_expenses_as_not_auth_user(self):
        self.client.force_authenticate(user=None)
        response = self.patch_expenses(1002)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_expenses_by_not_owner(self):
        self.client.force_authenticate(user=self.ex_4_user)
        response = self.patch_expenses(1005)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_expenses_by_owner(self):
        id = 1005
        self.client.force_authenticate(user=self.ex_3_user)
        response = self.patch_expenses(id)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        content = json.loads(response.content)
        expenses = Expenses.objects.select_related("item").get(pk=id)
        serializer = ExpensesSerializer(expenses)

        self.assertEqual(content["cost"], self.data_patch["cost"])
        self.assertEqual(serializer.data["cost"], self.data_patch["cost"])

        self.assertEqual(expenses.item.name, self.data_patch["item"])
        self.assertEqual(content["item"], self.data_patch["item"])

        self.assertEqual(content["date"], self.data_patch["date"])
        self.assertEqual(expenses.date.strftime("%Y-%m-%d"), self.data_patch["date"])

        self.assertEqual(content["time"][:-3], self.data_patch["time"])
        self.assertEqual(expenses.time.strftime("%H:%M"), self.data_patch["time"])

    def test_patch_expenses_with_wrong_user_id_by_owner(self):
        id = 1003
        self.data_patch["user"] = 10003
        self.client.force_authenticate(user=self.ex_3_user)
        response = self.patch_expenses(id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def patch_expenses(self, id):
        url = reverse("expenses:expenses_detail", kwargs={"pk": id})
        return self.client.patch(url, self.data_patch)

    def test_get_expenses_list_as_not_auth_user(self):
        self.client.force_authenticate(user=None)
        response = self.get_expenses_list()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_expenses_list_as_auth_user(self):
        self.client.force_authenticate(user=self.ex_3_user)
        response = self.get_expenses_list()
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def get_expenses_list(self):
        url = reverse("expenses:expenses_list_or_create")
        return self.client.get(url)

    def test_delete_expenses_as_not_auth_user(self):
        self.client.force_authenticate(user=None)
        response = self.delete_expenses(1008)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_expenses_by_owner(self):
        self.client.force_authenticate(user=self.ex_3_user)
        response = self.delete_expenses(1006)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_expenses_by_not_owner(self):
        self.client.force_authenticate(user=self.ex_4_user)
        response = self.delete_expenses(1005)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def delete_expenses(self, id):
        url = reverse("expenses:expenses_detail", kwargs={"pk": id})
        return self.client.delete(url)
