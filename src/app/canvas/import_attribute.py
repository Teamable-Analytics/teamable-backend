from typing import Dict, List

from canvasapi import Canvas
from canvasapi.assignment import Assignment, AssignmentGroup

from app.models.attribute import (
    Attribute,
    AttributeManageType,
    AttributeOption,
    AttributeResponse,
    AttributeValueType,
)
from app.models.course import Course
from app.models.course_member import UserRole
from app.models.organization import LMSTypeOptions
from app.views import attribute

ABOVE_AVERAGE_LABEL = "Above Average"
BELOW_AVERAGE_LABEL = "Below Average"


# Study buddy specific function
def get_or_create_gradebook_attribute(course: Course, assignment: Assignment):
    attribute_name = f"{assignment.name} - {assignment.id}"

    if course.attributes.filter(
        name=attribute_name, manage_type=AttributeManageType.GRADE
    ).exists():
        return course.attributes.get(name=attribute_name)

    attribute = Attribute.objects.create(
        name=attribute_name,
        question="",
        value_type=AttributeValueType.STRING,
        max_selections=1,
        course=course,
        manage_type=AttributeManageType.GRADE,
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

    return attribute


# Study buddy specific function
def import_gradebook_attribute_from_canvas(course: Course):
    if (
        course.organization is None
        or course.organization.lms_type != LMSTypeOptions.CANVAS
    ):
        return

    canvas = Canvas(course.organization.lms_api_url, course.lms_access_token)
    canvas_course = canvas.get_course(course.lms_course_id)

    course_members = course.course_members.filter(role=UserRole.STUDENT)
    assignments: List[Assignment] = list(canvas_course.get_assignments())

    for assignment in assignments:
        if assignment.grading_type != "points":
            continue

        if not assignment.points_possible:
            continue

        submissions = list(assignment.get_submissions())
        submission_grade = [
            (
                course_members.get(lms_id=submission.user_id),
                submission.score if submission.score is not None else 0,
            )
            for submission in submissions
            if course_members.filter(lms_id=submission.user_id).exists()
        ]

        sorted_members = [
            course_member
            for (course_member, _) in sorted(submission_grade, key=lambda x: x[1])
        ]
        median_index = (len(sorted_members) + 1) // 2

        attribute = get_or_create_gradebook_attribute(course, assignment)
        above_option = attribute.options.get(value="Above")
        below_option = attribute.options.get(value="Below")

        for i, course_member in enumerate(sorted_members):
            attribute_option = above_option if i >= median_index else below_option
            AttributeResponse.objects.update_or_create(
                course_member=course_member,
                attribute_option__attribute=attribute,
                defaults={
                    "attribute_option_id": attribute_option.pk,
                },
                create_defaults={
                    "attribute_option_id": attribute_option.pk,
                },
            )
