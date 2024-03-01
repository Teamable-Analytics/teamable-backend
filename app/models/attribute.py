from django.db import models

from app.models.base_models import BaseModel
from app.models.course_member import CourseMember


class AttributeValueType(models.TextChoices):
    STRING = "String", "String"
    NUMBER = "Number", "Number"
    TEAM_TEMPLATE_SLUG = "TeamTemplateSlug", "TeamTemplateSlug"


class Attribute(BaseModel):
    question = models.TextField()
    value_type = models.CharField(max_length=50, choices=AttributeValueType.choices)
    max_selections = models.IntegerField()
    team_set_template = models.ForeignKey(
        "app.TeamSetTemplate",
        on_delete=models.CASCADE,
        null=True,
        related_name="attributes",
    )
    course = models.ForeignKey(
        "app.Course", on_delete=models.CASCADE, related_name="attributes"
    )


class AttributeOption(BaseModel):
    attribute = models.ForeignKey(
        Attribute, on_delete=models.CASCADE, related_name="options"
    )
    value = models.TextField()


class AttributeResponse(BaseModel):
    course_member = models.ForeignKey(
        CourseMember, on_delete=models.CASCADE, related_name="attribute_responses"
    )
    attribute_option = models.ForeignKey(
        AttributeOption, on_delete=models.CASCADE, related_name="attribute_responses"
    )
