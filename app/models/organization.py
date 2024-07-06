from django.db import models

from app.models.base_models import BaseModel


class LMSTypeOptions(models.TextChoices):
    CANVAS = "CANVAS"


class Organization(BaseModel):
    name = models.CharField(max_length=500)

    lms_type = models.CharField(
        max_length=500, choices=LMSTypeOptions.choices, null=True, blank=True
    )
    lms_api_url = models.CharField(max_length=500, null=True, blank=True)
    lms_access_token = models.CharField(max_length=500, null=True, blank=True)
    lms_course_id = models.CharField(max_length=500, null=True, blank=True)
