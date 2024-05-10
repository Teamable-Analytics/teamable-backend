from django.urls import include, path
from rest_framework import routers

from app.views.attribute import AttributeViewSet
from app.views.course import CourseViewSet
from app.views.course_member import CourseMemberViewSet
from app.views.relationship import RelationshipViewSet
from app.views.section import SectionViewSet
from app.views.course_sections import CourseSectionViewSet

from app.views.teams import (
    TeamViewSet,
    TeamSetViewSet,
    TeamSetTemplateViewSet,
    TeamTemplateViewSet,
    OutlinedTeamSetTemplateViewSet,
)

router = routers.DefaultRouter()
router.register("courses", CourseViewSet)
router.register("sections", SectionViewSet)
router.register("course-members", CourseMemberViewSet)
router.register("course-sections", CourseSectionViewSet)
router.register("relationships", RelationshipViewSet)
router.register("teams", TeamViewSet)
router.register("teamsets", TeamSetViewSet)
router.register("team-templates", TeamTemplateViewSet)
router.register("teamset-templates", TeamSetTemplateViewSet)
router.register("teamset-templates/outlined", OutlinedTeamSetTemplateViewSet)
router.register("attributes", AttributeViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "course-members/course/<int:course>/",
        CourseMemberViewSet.as_view({"get": "get_students_by_course"}),
        name="get-students-by-course",
    ),
    path(
        "course/<int:course>/sections/",
        CourseSectionViewSet.as_view({"get": "get_course_sections"}),
        name="get_course_sections",
    ),
]
