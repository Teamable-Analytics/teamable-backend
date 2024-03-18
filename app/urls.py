from django.urls import include, path
from rest_framework import routers

from app.views.course import CourseViewSet
from app.views.course_member import CourseMemberViewSet
from app.views.relationship import RelationshipViewSet
from app.views.section import SectionViewSet
from app.views.team import (
    TeamTemplateViewSet,
    TeamViewSet,
    TeamSetViewSet,
    TeamRequirementViewSet,
    TeamSetTemplateViewSet,
    TeamTemplateRequirementViewSet
)

router = routers.DefaultRouter()
router.register("courses", CourseViewSet)
router.register("sections", SectionViewSet)
router.register("course-members", CourseMemberViewSet)
router.register("relationships", RelationshipViewSet)
router.register("team-set", TeamSetViewSet)
router.register("team", TeamViewSet)
router.register("team-requirement", TeamRequirementViewSet)
router.register("team-set-template", TeamSetTemplateViewSet)
router.register("team_templates", TeamTemplateViewSet)
router.register("team-template-requirements", TeamTemplateRequirementViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
