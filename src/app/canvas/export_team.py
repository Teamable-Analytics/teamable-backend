from canvasapi import Canvas

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

    group_category = canvas_course.create_group_category(name=team_set.name)

    for i, team in enumerate(team_set.teams.all()):
        group = group_category.create_group(name=i)

        for member in team.members.all():
            member: CourseMember
            group.create_membership(member.lms_id)
