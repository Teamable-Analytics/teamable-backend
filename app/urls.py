from django.urls import include, path
from rest_framework import routers

from app.views.course import CourseViewSet
from app.views.enrollment import EnrollmentViewSet
from app.views.projects import ProjectViewSet, ProjectSetViewSet
from app.views.relationship import RelationshipViewSet
from app.views.section import SectionViewSet

router = routers.DefaultRouter()
router.register("courses", CourseViewSet)
router.register("sections", SectionViewSet)
router.register("enrollments", EnrollmentViewSet)
router.register("relationships", RelationshipViewSet)
router.register("projects", ProjectViewSet)
router.register("project-sets", ProjectSetViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
