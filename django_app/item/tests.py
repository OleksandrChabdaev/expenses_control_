import json
import logging

from django.urls import reverse
from rest_framework import status
from user.tests import UserBase

logger = logging.getLogger("root")


class ItemTestCase(UserBase):
    fixtures = [
        "user/fixtures/user_fixtures.json",
        "item/fixtures/item_fixtures.json",
    ]

    def setUp(self):
        super().setUp()
        self.data_create = {
            "name": "Item_test",
            "user": 1003,
        }

    def test_create_item_as_not_auth_user(self):
        url = reverse("item:item_list_or_create")
        self.client.force_authenticate(user=None)
        response = self.client.post(url, self.data_create)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_item_by_not_owner(self):
        url = reverse("item:item_list_or_create")
        self.client.force_authenticate(user=self.ex_4_user)
        response = self.client.post(url, self.data_create)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_item_by_owner(self):
        url = reverse("item:item_list_or_create")
        self.client.force_authenticate(user=self.ex_3_user)
        response = self.client.post(url, self.data_create)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_item_list_as_not_auth_user(self):
        self.client.force_authenticate(user=None)
        response = self.get_item_list()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_item_list_as_auth_user(self):
        self.client.force_authenticate(user=self.ex_3_user)
        response = self.get_item_list()
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def get_item_list(self):
        url = reverse("item:item_list_or_create")
        return self.client.get(url)
