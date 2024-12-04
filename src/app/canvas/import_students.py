from typing import List, Tuple

from canvasapi import Canvas
from canvasapi.enrollment import Enrollment
from canvasapi.quiz import QuizQuestion

from app.models.course import Course
from app.models.course_member import CourseMember, UserRole
from app.models.organization import LMSTypeOptions


def import_students_from_canvas(course: Course) -> Tuple[int, int]:
    if (
        course.organization is None
        or course.organization.lms_type != LMSTypeOptions.CANVAS
    ):
        return 0, 0

    canvas = Canvas(course.organization.lms_api_url, course.lms_access_token)
    canvas_course = canvas.get_course(course.lms_course_id)

    students: List[Enrollment] = list(
        canvas_course.get_enrollments(type=["StudentEnrollment"])
    )
    total_students = len(students)

    if course.lms_opt_in_quiz_id is not None:
        opted_in_ids = set()
        opt_in_quiz = canvas_course.get_quiz(course.lms_opt_in_quiz_id)

        questions: List[QuizQuestion] = list(opt_in_quiz.get_questions())
        correct_answer_id = next(
            a["id"] for a in questions[0].answers if a["weight"] == 100
        )

        responses = list(opt_in_quiz.get_submissions())
        for response in responses:
            # Assuming there is exactly 1 question and 1 submission per user
            # The correct answer is YES
            submission_question = response.get_submission_questions()[0]
            opt_in = False
            if hasattr(submission_question, "correct"):
                opt_in = submission_question.correct
            # This is fix for the weird case where the submission_question does not have a correct attribute
            elif hasattr(submission_question, "answer"):
                opt_in = submission_question.answer == correct_answer_id
            if opt_in:
                opted_in_ids.add(response.user_id)
        students = [
            student for student in students if student.user["id"] in opted_in_ids
        ]

    for student in students:
        last_name, first_name = student.user["sortable_name"].split(",")

        CourseMember.upsert_course_member(
            user_id=None,
            first_name=first_name,
            last_name=last_name,
            lms_id=student.user["id"],
            sis_user_id=(
                student.sis_user_id
                if hasattr(student, "sis_user_id") and student.sis_user_id is not None
                else None
            ),
            course_id=course.pk,
            role=UserRole.STUDENT,
        )

    return total_students, len(students)
