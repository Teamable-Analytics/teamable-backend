from typing import TYPE_CHECKING
from django.db import models

from app.models.base_models import BaseModel
from app.models.course_member import CourseMember

if TYPE_CHECKING:
    from django.db.models.manager import RelatedManager


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
        blank=True,
        # no related_name since it's not correct to say that a TeamTemplate has attributes
        # will mostly be accessing an Attribute's TeamSet
    )
    course = models.ForeignKey(
        "app.Course", on_delete=models.CASCADE, related_name="attributes"
    )
    managed = models.BooleanField(
        default=False,
        blank=True,
        help_text=(
            "Denotes that an attribute is managed manually. Students do not self-report this data, "
            "nor is it editable to the instructor in the same ways that a normal attribute would be."
        ),
    )

    @property
    def has_student_responses(self):
        return self.options.exists()

    @property
    def num_student_responses(self):
        return self.options.count()

    def delete_student_responses(self):
        return self.options.all().delete()

    if TYPE_CHECKING:
        options: RelatedManager["AttributeOption"]


class AttributeOption(BaseModel):
    attribute = models.ForeignKey(
        Attribute, on_delete=models.CASCADE, related_name="options"
    )
    label = models.TextField()
    value = models.TextField()

    if TYPE_CHECKING:
        attribute_responses: RelatedManager["AttributeResponse"]


class AttributeResponse(BaseModel):
    course_member = models.ForeignKey(
        CourseMember, on_delete=models.CASCADE, related_name="attribute_responses"
    )
    attribute_option = models.ForeignKey(
        AttributeOption, on_delete=models.CASCADE, related_name="attribute_responses"
    )
