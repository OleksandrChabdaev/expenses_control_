import requests
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.authentication import (SessionAuthentication,
                                           TokenAuthentication)
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from user.models import User
from user.permissions import IsOwnerPermission
from user.serializers import UserSerializer


class CustomAuth(TokenAuthentication):
    keyword = "Bearer"


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, IsOwnerPermission,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ("get", "patch")

    def patch(self, request, *args, **kwargs):
        if (
                int(request.data["user"]) != self.request.user.id
                and not self.request.user.is_superuser
        ):
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().patch(request, *args, **kwargs)


class GoogleAuthorizationAPIView(APIView):
    def post(self, request):
        payload = {"access_token": request.data.get("access_token")}  # validate the token
        r = requests.get("https://www.googleapis.com/oauth2/v2/userinfo", params=payload)

        data = json.loads(r.text)

        if "error" in data:
            return Response(
                {
                    "message": "Wrong google token / this google token is already expired."
                }
            )

        try:
            user = User.objects.get(email=data["email"])
        except User.DoesNotExist:
            user = User()
            user.username = data["email"].split("@")[0]
            user.password = make_password(BaseUserManager().make_random_password())
            user.email = data["email"]
            user.first_name = data.get('given_name')
            user.last_name = data.get('family_name')
            user.save()

        token = RefreshToken.for_user(user)
        return Response(
            {
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "access_token": str(token.access_token),
                "refresh_token": str(token),
                "avatar": str(data["picture"]),
                "id": user.id,
                "email": user.email,
                "day_sum": user.day_sum,
            }
        )


class GoogleLogoutAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
