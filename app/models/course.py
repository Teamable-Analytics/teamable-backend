from django.db import models

from app.models.base_models import BaseModel
from app.models.organization import Organization


class Course(BaseModel):
    name = models.CharField(max_length=500)
    organization = models.ForeignKey(Organization, null=True, blank=True, on_delete=models.SET_NULL)
