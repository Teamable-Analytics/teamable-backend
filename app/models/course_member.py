from django.contrib.auth.models import User
from django.db import models

from app.models.base_models import BaseModel
from django.utils.translation import gettext_lazy as _

from app.models.course import Course
from app.models.section import Section


class UserRole(models.TextChoices):
    STUDENT = "S", _("Student")
    INSTRUCTOR = "I", _("Instructor")


class CourseMember(BaseModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="course_memberships"
    )
    sections = models.ManyToManyField(Section, related_name="section_members")
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    role = models.CharField(max_length=1, choices=UserRole.choices)
    external_lms_id = models.CharField(max_length=100, blank=True)
