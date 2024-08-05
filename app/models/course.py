from django.db import models

from app.models.base_models import BaseModel
from app.models.organization import Organization
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.db.models.manager import RelatedManager
    from app.models.team import TeamSet
    from app.models.course_member import CourseMember
    from app.models.attribute import Attribute



class Course(BaseModel):
    name = models.CharField(max_length=500)
    organization = models.ForeignKey(
        Organization, null=True, blank=True, on_delete=models.SET_NULL
    )
    lms_access_token = models.CharField(max_length=500, null=True, blank=True)
    lms_course_id = models.CharField(max_length=500, null=True, blank=True)
    lms_opt_in_quiz_id = models.CharField(max_length=500, null=True, blank=True)

    # Studdy buddy specific fields
    grade_book_attribute = models.OneToOneField["Attribute"](
        "Attribute", on_delete=models.SET_NULL, null=True, blank=True, related_name="grade_book_course"
    )

    if TYPE_CHECKING:
        team_sets: RelatedManager[TeamSet]
        course_members: RelatedManager[CourseMember]
