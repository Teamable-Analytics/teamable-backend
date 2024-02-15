from django.urls import include, path
from rest_framework import routers

from app.views.course import CourseViewSet
from app.views.course_member import CourseMemberViewSet
from app.views.projects import ProjectViewSet, ProjectSetViewSet
from app.views.relationship import RelationshipViewSet
from app.views.section import SectionViewSet
from app.views.teams import TeamViewSet, TeamSetViewSet

router = routers.DefaultRouter()
router.register("courses", CourseViewSet)
router.register("sections", SectionViewSet)
router.register("course-members", CourseMemberViewSet)
router.register("relationships", RelationshipViewSet)
router.register("projects", ProjectViewSet)
router.register("project-sets", ProjectSetViewSet)
router.register("teams", TeamViewSet)
router.register("team-sets", TeamSetViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
