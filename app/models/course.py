from django.db import models

from app.models.base_models import BaseModel
from django.utils.translation import gettext_lazy as _


class LMSSystems(models.TextChoices):
    CANVAS = "CN", _("Canvas")


class Course(BaseModel):
    name = models.CharField(max_length=500)
    lms_system = models.CharField(
        max_length=2, choices=LMSSystems.choices, null=True
    )
