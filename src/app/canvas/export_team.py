from canvasapi import Canvas, exceptions
from canvasapi.course import Course
from canvasapi.group import GroupCategory

from app.models.course_member import CourseMember
from app.models.organization import LMSTypeOptions
from app.models.team import TeamSet


def export_team_to_canvas(team_set: TeamSet):
    course = team_set.course
    if (
        course.organization is None
        or course.organization.lms_type != LMSTypeOptions.CANVAS
    ):
        return

    canvas = Canvas(course.organization.lms_api_url, course.lms_access_token)
    canvas_course = canvas.get_course(course.lms_course_id)

    group_category = create_group_category_with_unique_name(
        canvas_course=canvas_course, base_name=team_set.name
    )

    for team in team_set.teams.all():
        group = group_category.create_group(name=team.name)

        for member in team.members.all():
            member: CourseMember
            if not member.lms_id:
                # fixme: this feels bad
                continue
            group.create_membership(int(member.lms_id))


# arbitrary limit so this does not run infinitely if the error is not the "same name" error
MAX_RETIRES = 20


def create_group_category_with_unique_name(
    canvas_course: Course, base_name: str
) -> GroupCategory:
    group_category = None
    counter = 1

    while group_category is None:
        try:
            name = f"{base_name} ({counter})" if counter > 1 else f"{base_name}"
            group_category = canvas_course.create_group_category(name=name)
        except exceptions.BadRequest as e:
            # fixme: we should probably be more specific about this error
            counter += 1
            if counter > MAX_RETIRES:
                raise e

    return group_category
