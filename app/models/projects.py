from django.db import models

from app.models.base_models import TimeStampedModel
from app.models.course import Course


class Project(TimeStampedModel):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500, blank=True)
    project_set_fk = models.ForeignKey(
        "ProjectSet", on_delete=models.CASCADE, related_name="projects"
    )


class ProjectSet(TimeStampedModel):
    name = models.CharField(max_length=100)
    course_fk = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name="course"
    )
