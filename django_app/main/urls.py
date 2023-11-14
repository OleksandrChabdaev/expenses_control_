from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework_swagger.views import get_swagger_view
from user.views import GoogleAuthorizationAPIView

schema = get_swagger_view(title="Expenses control")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("rest_framework.urls")),
    path("api/user/", include("user.urls")),
    path("api/expenses/", include("expenses.urls")),
    path("api/item/", include("item.urls")),
    path("api/google/", GoogleAuthorizationAPIView.as_view(), name="google_login"),
    path("docs/", schema),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
