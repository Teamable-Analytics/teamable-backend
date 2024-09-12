from django.db.models import QuerySet, Q

from app.models.attribute import Attribute, AttributeOption
from app.models.base_models import BaseModel
from django.db import models
from typing import TYPE_CHECKING
from app.models.course import Course
from app.models.course_member import CourseMember, UserRole

if TYPE_CHECKING:
    from django.db.models.manager import RelatedManager


class RequirementSubject(models.TextChoices):
    EVERYONE = "Everyone", "Everyone"
    SOMEONE = "Someone", "Someone"


class RequirementOperator(models.TextChoices):
    # todo: "OVERLAPS" and "NOT_OVERLAPS"
    GT = "GT", "Greater Than"
    GTE = "GTE", "Greater Than or Equal"
    LT = "LT", "Less Than"
    LTE = "LTE", "Less Than or Equal"
    IN = "IN", "In"
    NOT_IN = "NOT_IN", "Not In"
    CONTAINS = "CONTAINS", "Contains"
    EQ = "EQ", "Equal"


class TeamSet(BaseModel):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="team_sets"
    )
    name = models.CharField(max_length=250)

    if TYPE_CHECKING:
        teams: RelatedManager["Team"]

    @property
    def assigned_students(self) -> QuerySet[CourseMember]:
        return self.course.course_members.filter(
            role=UserRole.STUDENT,
            teams__team_set=self
        ).distinct()

    @property
    def unassigned_students(self) -> QuerySet[CourseMember]:
        assigned_course_members = self.assigned_students
        return self.course.course_members.filter(
            Q(role=UserRole.STUDENT),
            ~Q(id__in=assigned_course_members)
        )


class Team(BaseModel):
    slug = models.UUIDField()
    name = models.CharField(max_length=250)
    max_people = models.IntegerField()
    min_people = models.IntegerField()
    members = models.ManyToManyField(CourseMember, related_name="teams")
    team_set = models.ForeignKey(
        TeamSet, on_delete=models.CASCADE, related_name="teams"
    )


class TeamRequirement(BaseModel):
    team = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name="requirements"
    )
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    operator = models.CharField(max_length=50, choices=RequirementOperator.choices)
    subject = models.CharField(max_length=20, choices=RequirementSubject.choices)
    options = models.ManyToManyField(AttributeOption)


class TeamSetTemplate(BaseModel):
    name = models.CharField(max_length=250)


class TeamTemplate(BaseModel):
    description = models.TextField()
    slug = models.UUIDField()
    number_of_teams = models.IntegerField()
    max_people = models.IntegerField()
    min_people = models.IntegerField()
    team_set = models.ForeignKey(
        TeamSetTemplate, on_delete=models.CASCADE, related_name="teams"
    )


class TeamTemplateRequirement(BaseModel):
    team_template = models.ForeignKey(
        TeamTemplate, on_delete=models.CASCADE, related_name="requirements"
    )
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    operator = models.CharField(max_length=50, choices=RequirementOperator.choices)
    subject = models.CharField(max_length=20, choices=RequirementSubject.choices)
    options = models.ManyToManyField(AttributeOption)
