from django.db import models

from accounts.models import MyUser
from app.models.base_models import BaseModel
from app.models.course import Course
from app.models.section import Section


class UserRole(models.TextChoices):
    STUDENT = "Student", "Student"
    INSTRUCTOR = "Instructor", "Instructor"


class CourseMember(BaseModel):
    user = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        related_name="course_memberships",
        null=True,
        blank=True,
    )
    sections = models.ManyToManyField(Section, related_name="section_members", blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, choices=UserRole.choices)
    name = models.CharField(max_length=50, null=True, blank=True)
    lms_id = models.CharField(max_length=50, null=True, blank=True, unique=True)

    @classmethod
    def add_course_member(
        cls,
        user_id: str | None,
        name: str,
        lms_id: str,
        course_id: str,
        role: UserRole
    ):
        course_member = cls.objects.get_or_create(
            lms_id=lms_id,
            defaults={
                "user_id": user_id,
                "name": name,
                "course_id": course_id,
                "role": role
            }
        )
        return course_member
