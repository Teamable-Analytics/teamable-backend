from django.db import models
from django.db.models import F

from accounts.models import MyUser
from app.models.base_models import BaseModel
from app.models.course import Course
from app.models.section import Section

class UserRole(models.TextChoices):
    STUDENT = "Student", "Student"
    INSTRUCTOR = "Instructor", "Instructor"


class CourseMember(BaseModel):
    user = models.ForeignKey(
        MyUser, on_delete=models.CASCADE, related_name="course_memberships"
    )
    sections = models.ManyToManyField(Section, related_name="section_members")
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, choices=UserRole.choices)