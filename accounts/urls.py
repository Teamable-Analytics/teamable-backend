from rest_framework import routers

from accounts.views import UserViewSet
from django.urls import include, path
from rest_framework.authtoken import views


router = routers.DefaultRouter()
router.register("users", UserViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("api-token-auth/", views.obtain_auth_token),
]
