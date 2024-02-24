from django.db import models

from app.models.base_models import BaseModel


class Course(BaseModel):
    name = models.CharField(max_length=500)
