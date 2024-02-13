from django.urls import include, path
from rest_framework import routers

from app.views.course import CourseViewSet
from app.views.section import SectionViewSet

router = routers.DefaultRouter()
router.register("courses", CourseViewSet)
router.register("sections", SectionViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
