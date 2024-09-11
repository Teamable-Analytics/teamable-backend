from django.db import models
from django.conf import settings
import jwt
from accounts.models import MyUser
from app.models.base_models import BaseModel
from app.models.course import Course
from app.models.organization import LMSTypeOptions
from app.models.section import Section


class UserRole(models.TextChoices):
    STUDENT = "Student", "Student"
    INSTRUCTOR = "Instructor", "Instructor"


class CourseMemberTokenError(Exception):
    """Custom exception class for handling token errors"""

    pass


class CourseMember(BaseModel):
    user = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        related_name="course_memberships",
        null=True,
        blank=True,
    )
    sections = models.ManyToManyField(
        Section, related_name="section_members", blank=True
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="course_members"
    )
    role = models.CharField(max_length=50, choices=UserRole.choices)
    name = models.CharField(max_length=50, null=True, blank=True)
    lms_id = models.CharField(max_length=50, null=True, blank=True)
    sis_user_id = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['course', 'lms_id'], name='unique_lms_id_in_course'),
            models.UniqueConstraint(fields=['course', 'sis_user_id'], name='unique_sis_user_id_in_course')
        ]

    @property
    def lms_link(self):
        org = self.course.organization
        if org.lms_type == LMSTypeOptions.CANVAS:
            if not org.lms_api_url or not self.course.lms_course_id or not self.lms_id:
                return None
            return f"{org.lms_api_url}/courses/{self.course.lms_course_id}/users/{self.lms_id}"
        return None

    def create_jwt_token(self):
        """
        Create a jwt token for a course member
        """
        token = jwt.encode(
            {"course_member_id": self.pk}, settings.SECRET_KEY, algorithm="HS256"
        )
        return token

    @classmethod
    def validate_token(cls, token) -> "CourseMember":
        """
        Validate a jwt token
        @return: the course member corresponding to the token
        """
        try:
            course_member_id = jwt.decode(
                token, settings.SECRET_KEY, algorithms=["HS256"]
            )["course_member_id"]
        except jwt.DecodeError:
            raise CourseMemberTokenError("Invalid token")

        course_member = cls.objects.get(id=course_member_id)

        if course_member.user is not None:
            raise CourseMemberTokenError("Course member already has a user")

        return course_member

    def set_user(self, user):
        self.user = user
        self.save()

    @classmethod
    def add_course_member(
        cls,
        user_id: str | None,
        name: str,
        lms_id: str,
        sis_user_id: str,
        course_id: str,
        role: UserRole,
    ):
        course_member = cls.objects.get_or_create(
            lms_id=lms_id,
            defaults={
                "user_id": user_id,
                "name": name,
                "course_id": course_id,
                "role": role,
                "sis_user_id": sis_user_id,
            },
        )
        return course_member
