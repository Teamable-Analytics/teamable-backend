from django.test import TestCase

from accounts.models import MyUser
from app.models.course import Course
from app.models.course_member import CourseMember, UserRole
from app.models.organization import Organization


class UpsertCourseMemberTests(TestCase):
    def setUp(self):
        org = Organization.objects.create(name="UBC")
        self.course_a = Course.objects.create(name="A", organization=org)
        self.course_b = Course.objects.create(name="B", organization=org)

    def upsert(self, course, lms_id="42", first_name="Ada"):
        return CourseMember.upsert_course_member(
            user_id=None,
            first_name=first_name,
            last_name="Lovelace",
            lms_id=lms_id,
            sis_user_id=None,
            course_id=course.pk,
            role=UserRole.STUDENT,
        )

    def test_same_lms_id_in_two_courses_creates_separate_members(self):
        self.upsert(self.course_a)
        self.upsert(self.course_b)

        self.assertEqual(self.course_a.course_members.count(), 1)
        self.assertEqual(self.course_b.course_members.count(), 1)

        # Re-importing must not fail now that the lms_id exists twice
        _, created = self.upsert(self.course_b, first_name="Augusta")
        self.assertFalse(created)
        self.assertEqual(self.course_b.course_members.get().first_name, "Augusta")
        self.assertEqual(self.course_a.course_members.get().first_name, "Ada")

    def test_existing_member_keeps_user_and_role(self):
        user = MyUser.objects.create(username="42+canvas")
        CourseMember.objects.create(
            user=user, course=self.course_a, lms_id="42", role=UserRole.INSTRUCTOR
        )

        self.upsert(self.course_a)

        member = self.course_a.course_members.get()
        self.assertEqual(member.user, user)
        self.assertEqual(member.role, UserRole.INSTRUCTOR)
