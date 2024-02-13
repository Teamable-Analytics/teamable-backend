from django.db import models

from app.models.base_models import TimeStampedModel
from django.utils.translation import gettext_lazy as _


class LMSSystems(models.TextChoices):
    OTHER = "O", _("Other")
    CANVAS = "CN", _("Canvas")


class Course(TimeStampedModel):
    name = models.CharField(max_length=500)
    lms_system = models.CharField(
        max_length=2, choices=LMSSystems.choices, default=LMSSystems.OTHER
    )
