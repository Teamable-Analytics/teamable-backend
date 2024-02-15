from django.db import models

from app.models.base_models import BaseModel
from app.models.course import Course


class Project(BaseModel):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500, blank=True)
    project_set_fk = models.ForeignKey(
        "ProjectSet", on_delete=models.CASCADE, related_name="projects"
    )


class ProjectSet(BaseModel):
    name = models.CharField(max_length=100)
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="project_sets"
    )
