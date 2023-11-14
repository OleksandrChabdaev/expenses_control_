from django.urls import include, path
from rest_framework import routers

from .views import UserRetrieveUpdateAPIView

app_name = "user"
router = routers.DefaultRouter()

urlpatterns = [
    path("", include(router.urls)),
    path("<int:pk>/", UserRetrieveUpdateAPIView.as_view(), name="user_detail"),
]
