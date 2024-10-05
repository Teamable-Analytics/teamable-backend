from django.db import models

from app.models.base_models import BaseModel
from app.models.course import Course


class Section(BaseModel):
    name = models.CharField(max_length=500)
    description = models.CharField(max_length=500, blank=True)
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="sections"
    )

    def __str__(self) -> str:
        return f"({self.pk}) {self.name}"
