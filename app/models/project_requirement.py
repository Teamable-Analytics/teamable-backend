import enum
from typing import TypeVar

from django.db import models

from app.models import Attribute
from app.models.base_models import BaseModel
from app.models.team import RequirementOperator, RequirementSubject


class ProjectRequirementType(models.TextChoices):
    NUMERIC_COMPARATIVE = "Numeric Comparative"


class ProjectRequirement(BaseModel):
    requirement_type = models.CharField(max_length=50, choices=ProjectRequirementType.choices)

    class Meta:
        abstract = True


class NumericComparativeProjectRequirement(ProjectRequirement):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    operator = models.CharField(max_length=50, choices=RequirementOperator.choices)
    value = models.IntegerField()
    project = models.ForeignKey('app.Project', on_delete=models.CASCADE, related_name='requirements')


ProjectRequirementSubclass = TypeVar('ProjectRequirementSubclass', bound=ProjectRequirement)


class ProjectRequirementFactory:
    @staticmethod
    def get_project_requirement(data) -> ProjectRequirementSubclass:
        requirement_type = data.get('requirement_type')
        if requirement_type == ProjectRequirementType.NUMERIC_COMPARATIVE.value:
            return NumericComparativeProjectRequirement(**data)
        elif requirement_type in ProjectRequirementType:
            raise ValueError("Not Implemented")
        else:
            raise ValueError("Invalid requirement type")
