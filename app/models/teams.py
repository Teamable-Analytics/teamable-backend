from django.db import models

from app.models.base_models import BaseModel
from app.models.course import Course
from app.models.course_member import CourseMember
from app.models.projects import Project
from app.models.section import Section


class TeamSet(BaseModel):
    name = models.CharField(max_length=500)
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="team_sets"
    )
    section = models.ForeignKey(
        Section, on_delete=models.CASCADE, related_name="team_sets"
    )


class Team(BaseModel):
    name = models.CharField(max_length=500)
    members = models.ManyToManyField(CourseMember, related_name="teams")
    team_set = models.ForeignKey(
        TeamSet, on_delete=models.CASCADE, related_name="teams"
    )
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="teams", null=True
    )
