from rest_framework import routers

from accounts.views import UserViewSet
from django.urls import include, path

router = routers.DefaultRouter()
router.register("users", UserViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
