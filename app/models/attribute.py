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
        return AttributeResponse.objects.filter(
            attribute_option__attribute=self
        ).exists()
        # return self.num_student_responses > 0

    @property
    def num_student_responses(self):
        # return AttributeResponse.objects.filter(
        #     attribute_option__attribute=self
        # ).count()
        print(self.options)
        return "self.options"
        # return self.attribute_options.aggregate(
        #     num_student_responses=models.Count("attribute_responses")
        # )["num_student_responses"]


class AttributeOption(BaseModel):
    attribute = models.ForeignKey(
        Attribute, on_delete=models.CASCADE, related_name="options"
    )
    label = models.TextField()
    value = models.TextField()

    @property
    def has_student_responses(self):
        return AttributeResponse.objects.filter(attribute_option=self).exists()

    @property
    def num_student_responses(self):
        # return AttributeResponse.objects.filter(attribute_option=self).count()
        return self.attribute


class AttributeResponse(BaseModel):
    course_member = models.ForeignKey(
        CourseMember, on_delete=models.CASCADE, related_name="attribute_responses"
    )
    attribute_option = models.ForeignKey(
        AttributeOption, on_delete=models.CASCADE, related_name="attribute_responses"
    )

    @staticmethod
    def clear_attribute_responses(attribute_id):
        num_attribute_responses_deleted, _ = AttributeResponse.objects.filter(
            attribute_option_id=attribute_id
        ).delete()
        return num_attribute_responses_deleted
