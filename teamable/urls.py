from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("api/accounts/", include("accounts.urls")),
    path("admin/", admin.site.urls),
    path("api/auth/", include("rest_framework.urls")),
]
