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

    canvas = Canvas(course.organization.lms_api_url, course.lms_access_token)
    canvas_course = canvas.get_course(course.lms_course_id)

    students: List[Enrollment] = list(
        canvas_course.get_enrollments(type=["StudentEnrollment"])
    )

    if course.lms_opt_in_quiz_id is not None:
        opted_in_ids = set()
        opt_in_quiz = canvas_course.get_quiz(course.lms_opt_in_quiz_id)
        responses = list(opt_in_quiz.get_submissions())
        for response in responses:
            # Assuming there is exactly 1 question and 1 submission per user
            # The correct answer is YES
            opt_in = response.get_submission_questions()[0].correct
            if opt_in:
                opted_in_ids.add(response.user_id)
        students = [
            student for student in students if student.user["id"] in opted_in_ids
        ]

    for student in students:
        CourseMember.add_course_member(
            user_id=None,
            name=student.user["name"],
            lms_id=student.user["id"],
            course_id=course.pk,
            role=UserRole.STUDENT,
        )
