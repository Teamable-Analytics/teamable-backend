from rest_framework.test import APITestCase

from accounts.models import MyUser
from app.models.course import Course
from app.models.course_member import CourseMember, UserRole
from app.models.organization import Organization


class CourseStudentsEndpointTests(APITestCase):
    def setUp(self):
        org = Organization.objects.create(name="UBC")
        self.course = Course.objects.create(name="BIOC 202", organization=org)
        instructor = MyUser.objects.create(username="instructor")
        CourseMember.objects.create(
            user=instructor, course=self.course, role=UserRole.INSTRUCTOR
        )
        CourseMember.objects.create(
            course=self.course,
            role=UserRole.STUDENT,
            first_name="Ada",
            last_name="Lovelace",
            lms_id="42",
            sis_user_id="1234",
        )
        self.client.force_authenticate(instructor)

    def test_students_are_serialized_as_course_members(self):
        response = self.client.get(f"/api/v1/courses/{self.course.pk}/students/")

        self.assertEqual(response.status_code, 200)
        student = response.json()["results"][0]
        self.assertEqual(student["first_name"], "Ada")
        self.assertEqual(student["last_name"], "Lovelace")
        self.assertEqual(student["sis_user_id"], "1234")
