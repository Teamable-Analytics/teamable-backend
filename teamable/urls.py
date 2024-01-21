from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("api/v1/accounts/", include("accounts.urls")),
    path("api/v1/", include("app.urls")),
    path("admin/", admin.site.urls),
    path("api/auth/", include("rest_framework.urls")),
]
