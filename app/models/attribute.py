from django.db import models

from app.models.base_models import BaseModel
from app.models.course_member import CourseMember


class AttributeValueType(models.TextChoices):
    STRING = "String", "String"
    NUMBER = "Number", "Number"
    TEAM_TEMPLATE_SLUG = "TeamTemplateSlug", "TeamTemplateSlug"


class Attribute(BaseModel):
    name = models.TextField()
    question = models.TextField()
    value_type = models.CharField(max_length=50, choices=AttributeValueType.choices)
    max_selections = models.IntegerField()
    team_set_template = models.ForeignKey(
        "app.TeamSetTemplate",
        on_delete=models.CASCADE,
        null=True,
        # no related_name since it's not correct to say that a TeamTemplate has attributes
        # will mostly be accessing an Attribute's TeamSet
    )
    course = models.ForeignKey(
        "app.Course", on_delete=models.CASCADE, related_name="attributes"
    )

    @property
    def has_student_responses(self):
        return self.num_student_responses > 0

    @property
    def num_student_responses(self):
        return AttributeResponse.objects.filter(
            attribute_option__attribute=self
        ).count()

    def delete_student_responses(self):
        num_deleted_attribute_responses, _ = AttributeResponse.objects.filter(
            attribute_option__attribute=self
        ).delete()
        return num_deleted_attribute_responses


class AttributeOption(BaseModel):
    attribute = models.ForeignKey(
        Attribute, on_delete=models.CASCADE, related_name="options"
    )
    label = models.TextField()
    value = models.TextField()


class AttributeResponse(BaseModel):
    course_member = models.ForeignKey(
        CourseMember, on_delete=models.CASCADE, related_name="attribute_responses"
    )
    attribute_option = models.ForeignKey(
        AttributeOption, on_delete=models.CASCADE, related_name="attribute_responses"
    )
