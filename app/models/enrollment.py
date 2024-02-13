from django.contrib.auth.models import User
from django.db import models

from app.models.base_models import TimeStampedModel
from django.utils.translation import gettext_lazy as _

from app.models.course import Course
from app.models.section import Section


class UserRole(models.TextChoices):
    STUDENT = "S", _("Student")
    INSTRUCTOR = "I", _("Instructor")
    TA = "T", _("TA")


class Enrollment(TimeStampedModel):
    """
    Models a user's involvement in a section (or group).
    A user can be in many sections.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sections = models.ManyToManyField(Section)
    course_fk = models.ForeignKey(Course, on_delete=models.CASCADE)
    role = models.CharField(max_length=1, choices=UserRole.choices)
    lms_id = models.CharField(max_length=100, blank=True)
