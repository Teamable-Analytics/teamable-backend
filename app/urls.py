from django.urls import include, path
from rest_framework import routers

from app.views.course import CourseViewSet
from app.views.enrollment import EnrollmentViewSet
from app.views.relationship import RelationshipViewSet
from app.views.section import SectionViewSet

router = routers.DefaultRouter()
router.register("courses", CourseViewSet)
router.register("sections", SectionViewSet)
router.register("enrollments", EnrollmentViewSet)
router.register("relationships", RelationshipViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
