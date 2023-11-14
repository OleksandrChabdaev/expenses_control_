from django.urls import path

from .views import ItemListCreateAPIView

app_name = "item"
urlpatterns = [path("", ItemListCreateAPIView.as_view(), name="item_list_or_create")]
