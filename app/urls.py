from rest_framework import routers

from accounts.views import UserViewSet
from django.urls import include, path

from app.views import CourseViewSet, StudentViewSet

router = routers.DefaultRouter()
router.register("courses", CourseViewSet)
router.register("students", StudentViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
