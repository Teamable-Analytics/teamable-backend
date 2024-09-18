from typing import Dict, List

from canvasapi import Canvas
from canvasapi.assignment import Assignment, AssignmentGroup

from app.models.attribute import (
    Attribute,
    AttributeOption,
    AttributeResponse,
    AttributeValueType,
)
from app.models.course import Course
from app.models.course_member import UserRole
from app.models.organization import LMSTypeOptions

ABOVE_AVERAGE_LABEL = "Above Average"
BELOW_AVERAGE_LABEL = "Below Average"


# Study buddy specific function
def create_gradebook_attribute(course: Course):
    if (
        course.organization is None
        or course.organization.lms_type != LMSTypeOptions.CANVAS
    ):
        return

    attribute = Attribute.objects.create(
        name="Gradebook",
        question="Gradebook?",
        value_type=AttributeValueType.STRING,
        max_selections=1,
        course=course,
    )

    AttributeOption.objects.create(
        attribute=attribute,
        label=ABOVE_AVERAGE_LABEL,
        value="Above",
    )

    AttributeOption.objects.create(
        attribute=attribute,
        label=BELOW_AVERAGE_LABEL,
        value="Below",
    )

    course.grade_book_attribute = attribute
    course.save()


# Study buddy specific function
def import_gradebook_attribute_from_canvas(course: Course):
    if (
        course.organization is None
        or course.organization.lms_type != LMSTypeOptions.CANVAS
    ):
        return

    if course.grade_book_attribute is None:
        create_gradebook_attribute(course)
    assert course.grade_book_attribute is not None

    canvas = Canvas(course.organization.lms_api_url, course.lms_access_token)
    canvas_course = canvas.get_course(course.lms_course_id)

    course_members = course.course_members.filter(role=UserRole.STUDENT)
    assignments: List[Assignment] = list(canvas_course.get_assignments())
    assignment_groups: List[AssignmentGroup] = list(
        canvas_course.get_assignment_groups()
    )

    student_grades: Dict[int, float] = {}
    assignment_group_weights: Dict[int, float] = {}
    assignment_group_totals: Dict[int, float] = {}

    for group in assignment_groups:
        assignment_group_weights[group.id] = group.group_weight
        assignment_group_totals[group.id] = 0

    for assignment in assignments:
        if assignment.grading_type != "points":
            continue

        points_possible = (
            assignment.points_possible if assignment.points_possible else 0
        )
        assignment_group_totals[assignment.assignment_group_id] += points_possible

    for student in course_members:
        student_grades[student.pk] = 0

    for student in course_members:
        for assignment in assignments:
            if assignment.grading_type != "points":
                continue

            if not assignment.points_possible:
                continue

            weight = assignment_group_weights[assignment.assignment_group_id]
            total = assignment_group_totals[assignment.assignment_group_id]

            try:
                grade = float(assignment.get_submission(student.lms_id).score)
            except Exception as e:
                grade = 0

            student_grades[student.pk] += (grade * weight / total) if total else 0

    average_grade = sum(student_grades.values()) / len(student_grades)

    above_option = course.grade_book_attribute.options.get(value="Above")
    below_option = course.grade_book_attribute.options.get(value="Below")

    for student in course_members:
        if student_grades[student.pk] >= average_grade:
            AttributeResponse.objects.update_or_create(
                course_member=student,
                defaults={
                    "attribute_option_id": above_option.pk,
                },
                create_defaults={
                    "attribute_option_id": above_option.pk,
                },
            )
        else:
            AttributeResponse.objects.update_or_create(
                course_member=student,
                defaults={
                    "attribute_option_id": below_option.pk,
                },
                create_defaults={
                    "attribute_option_id": below_option.pk,
                },
            )
