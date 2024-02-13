from django.db import models

from app.models.base_models import TimeStampedModel
from app.models.course import Course


class Section(TimeStampedModel):
    name = models.CharField(max_length=500)
    description = models.CharField(max_length=500, blank=True)
    course_fk = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="sections"
    )
