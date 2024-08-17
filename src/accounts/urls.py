from rest_framework import routers

from accounts.views import UserLoginViewSet, UserRegistrationViewSet, UserViewSet
from django.urls import include, path


router = routers.DefaultRouter()
router.register("users", UserViewSet, basename="user")
router.register("sign-up", UserRegistrationViewSet, basename="sign-up")
router.register("log-in", UserLoginViewSet, basename="log-in")

urlpatterns = [
    path("", include(router.urls)),
]
