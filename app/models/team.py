from app.models.attribute import Attribute, AttributeOption
from app.models.base_models import BaseModel
from django.db import models

from app.models.course_member import CourseMember


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
    name = models.CharField(max_length=250)


class Team(BaseModel):
    slug = models.UUIDField()
    max_people = models.IntegerField()
    min_people = models.IntegerField()
    members = models.ManyToManyField(CourseMember, related_name="teams")


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


class TeamTemplateRequirement(BaseModel):
    team_template = models.ForeignKey(
        TeamTemplate, on_delete=models.CASCADE, related_name="requirements"
    )
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    operator = models.CharField(max_length=50, choices=RequirementOperator.choices)
    subject = models.CharField(max_length=20, choices=RequirementSubject.choices)
    options = models.ManyToManyField(AttributeOption)
