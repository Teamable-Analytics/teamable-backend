from django.db import models
from django.db.models import Count

from app.models.base_models import BaseModel
from app.models.organization import Organization, LMSTypeOptions
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.db.models.manager import RelatedManager
    from app.models.team import TeamSet
    from app.models.course_member import CourseMember, UserRole
    from app.models.attribute import Attribute
    from accounts.models import MyUser


class Course(BaseModel):
    name = models.CharField(max_length=500)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    lms_access_token = models.CharField(max_length=500, null=True, blank=True)
    lms_course_id = models.CharField(max_length=500, null=True, blank=True)
    lms_opt_in_quiz_id = models.CharField(max_length=500, null=True, blank=True)

    if TYPE_CHECKING:
        team_sets: RelatedManager[TeamSet]
        course_members: RelatedManager[CourseMember]
        attributes: RelatedManager[Attribute]

    def has_view_permission(self, user: "MyUser") -> bool:
        return True

    def has_edit_permission(self, user: "MyUser") -> bool:
        if not user.is_authenticated:
            return False
        if self.is_instructor(user):
            return True
        if user.is_staff:
            return True
        return False

    def is_instructor(self, user: "MyUser") -> bool:
        from app.models.course_member import UserRole

        return self.course_members.filter(user=user, role=UserRole.INSTRUCTOR).exists()

    @property
    def opt_in_quiz_link(self):
        if not self.lms_opt_in_quiz_id:
            return None
        if not self.organization.lms_api_url:
            return None
        if self.organization.lms_type != LMSTypeOptions.CANVAS:
            return None
        return f"{self.organization.lms_api_url}/courses/{self.lms_course_id}/quizzes/{self.lms_opt_in_quiz_id}"

    @property
    def has_created_opt_in_quiz(self):
        return self.lms_opt_in_quiz_id is not None

    @property
    def has_students(self):
        from app.models.course_member import UserRole

        return self.course_members.filter(role=UserRole.STUDENT.value).exists()

    @property
    def has_attribute(self):
        return self.attributes.exists()

    @property
    def has_attribute_responses(self):
        return (
            self.attributes.alias(num_responses=Count("options__attribute_responses"))
            .filter(num_responses__gt=0)
            .exists()
        )

    @property
    def has_team_set(self):
        return self.team_sets.exists()
