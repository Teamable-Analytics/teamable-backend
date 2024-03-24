from django.urls import include, path
from rest_framework import routers

from app.views.attribute import AttributeViewSet
from app.views.course import CourseViewSet
from app.views.course_member import CourseMemberViewSet
from app.views.relationship import RelationshipViewSet
from app.views.section import SectionViewSet
from app.views.teams import (
    TeamViewSet,
    TeamSetViewSet,
    TeamSetTemplateViewSet,
    TeamTemplateViewSet,
)

router = routers.DefaultRouter()
router.register("courses", CourseViewSet)
router.register("sections", SectionViewSet)
router.register("course-members", CourseMemberViewSet)
router.register("relationships", RelationshipViewSet)
router.register("teamsets/(?P<teamset_id>[^/.]+)/teams", TeamViewSet)
router.register("teamsets", TeamSetViewSet)
router.register("teamset-templates/(?P<teamset_template_id>[^/.]+)/team-templates", TeamTemplateViewSet)
router.register("teamset-templates", TeamSetTemplateViewSet)
router.register("attributes", AttributeViewSet)


urlpatterns = [
    path("", include(router.urls)),
]
