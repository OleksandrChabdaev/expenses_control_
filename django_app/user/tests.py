import json
import logging

from django.contrib.auth.models import Group
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

from .models import User
from .serializers import UserSerializer

logger = logging.getLogger("root")


class UserBase(APITestCase):
    @staticmethod
    def add_users_to_groups():
        group = Group.objects.get(name="Managers")
        user = User.objects.get(id=1002)
        user.groups.add(group)

        group = Group.objects.get(name="Regulars")
        user = User.objects.get(id=1003)
        user.groups.add(group)
        user = User.objects.get(id=1004)
        user.groups.add(group)

    def setUp(self):
        self.add_users_to_groups()
        self.staff_user = User.objects.get(id=1002)
        self.ex_3_user = User.objects.get(id=1003)
        self.ex_4_user = User.objects.get(id=1004)


class UserTestCase(UserBase):
    fixtures = [
        "user/fixtures/user_fixtures.json",
    ]

    def setUp(self):
        super().setUp()
        self.data_patch = {
            "first_name": "Oleksandr",
            "last_name": "Chabdaiev",
            "day_sum": 100,
        }

    def test_get_user_as_not_auth_user(self):
        self.client.force_authenticate(user=None)
        response = self.get_user(1003)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_user_by_not_owner(self):
        self.client.force_authenticate(user=self.ex_4_user)
        response = self.get_user(1003)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_user_by_manager(self):
        self.client.force_authenticate(user=self.staff_user)
        response = self.get_user(1003)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_by_owner(self):
        self.client.force_authenticate(user=self.ex_3_user)
        response = self.get_user(1003)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def get_user(self, id):
        url = reverse("user:user_detail", kwargs={"pk": id})
        return self.client.get(url)

    def test_patch_user_as_not_auth_user(self):
        self.client.force_authenticate(user=None)
        response = self.patch_user(1002)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_user_by_not_owner(self):
        self.client.force_authenticate(user=self.ex_4_user)
        response = self.patch_user(1003)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_user_by_manager(self):
        self.client.force_authenticate(user=self.staff_user)
        response = self.patch_user(1003)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        content = json.loads(response.content)
        user = User.objects.get(pk=1003)
        serializer = UserSerializer(user)

        self.assertEqual(content["day_sum"], self.data_patch["day_sum"])
        self.assertEqual(serializer.data["day_sum"], self.data_patch["day_sum"])

        self.assertEqual(content["first_name"], self.data_patch["first_name"])
        self.assertEqual(user.first_name, self.data_patch["first_name"])

        self.assertEqual(content["last_name"], self.data_patch["last_name"])
        self.assertEqual(user.first_name, self.data_patch["last_name"])

    def test_patch_user_by_owner(self):
        self.client.force_authenticate(user=self.ex_3_user)
        response = self.patch_user(1003)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        content = json.loads(response.content)
        user = User.objects.get(pk=1003)
        serializer = UserSerializer(user)

        self.assertEqual(content["day_sum"], self.data_patch["day_sum"])
        self.assertEqual(serializer.data["day_sum"], self.data_patch["day_sum"])

        self.assertEqual(content["first_name"], self.data_patch["first_name"])
        self.assertEqual(user.first_name, self.data_patch["first_name"])

        self.assertEqual(content["last_name"], self.data_patch["last_name"])
        self.assertEqual(user.first_name, self.data_patch["last_name"])

    def patch_user(self, id):
        url = reverse("user:user_detail", kwargs={"pk": id})
        return self.client.patch(url, self.data_patch)
