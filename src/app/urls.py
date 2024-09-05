from django.urls import include, path
from rest_framework import routers

from app.views.course import CourseViewSet
from app.views.course_sections import CourseSectionViewSet


router = routers.DefaultRouter()
router.register("courses", CourseViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "course/<int:course>/sections/",
        CourseSectionViewSet.as_view({"get": "get_course_sections"}),
        name="get_course_sections",
    ),
]
