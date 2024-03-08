from django.db import models

from app.models.base_models import BaseModel


class Project(BaseModel):
    name = models.CharField(max_length=500)
    number_of_teams = models.IntegerField()
    project_set = models.ForeignKey('app.ProjectSet', on_delete=models.CASCADE, related_name='projects')


class ProjectSet(BaseModel):
    name = models.CharField(max_length=250)
