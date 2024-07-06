from typing import List
from app.models.course import Course
from canvasapi import Canvas
from canvasapi.enrollment import Enrollment

from app.models.course_member import CourseMember, UserRole
from app.models.organization import LMSTypeOptions


def import_students_from_canvas(course: Course):
    if (
        course.organization is None
        or course.organization.lms_type != LMSTypeOptions.CANVAS
    ):
        return

    canvas = Canvas(
        course.organization.lms_api_url, course.organization.lms_access_token
    )
    canvas_course = canvas.get_course(course.organization.lms_course_id)

    students: List[Enrollment] = list(
        canvas_course.get_enrollments(type=["StudentEnrollment"])
    )

    for student in students:
        CourseMember.add_course_member(
            user_id=None,
            name=student.user["name"],
            lms_id=student.user["id"],
            course_id=course.pk,
            role=UserRole.STUDENT,
        )
