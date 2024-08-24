from app.canvas.import_attribute import ABOVE_AVERAGE_LABEL, BELOW_AVERAGE_LABEL
from app.models.course import Course
import requests
import uuid

from app.models.course_member import CourseMember
from app.models.team import Team, TeamSet

TEAM_GENERATION_API_URL = "https://api.teamableanalytics.ok.ubc.ca/api/generate/teams/"


def generate_teams(course: Course):
    attribute = course.grade_book_attribute

    if attribute is None:
        return

    above_average = attribute.options.get(label=ABOVE_AVERAGE_LABEL)
    below_average = attribute.options.get(label=BELOW_AVERAGE_LABEL)

    above_average_members = list(
        above_average.attribute_responses.values_list("course_member", flat=True)
    )
    below_average_members = list(
        below_average.attribute_responses.values_list("course_member", flat=True)
    )

    # req = requests.post(
    #     TEAM_GENERATION_API_URL,
    #     headers={
    #         "X-Api-Key": "CI4c69/IXGrczbtQYdfbjfoi+JjCXT1i54jzVQox8MA=",
    #     },
    #     json={
    #         "algorithm_options": {
    #             "algorithm_type": "weight",
    #             "max_project_preferences": 0,
    #             "requirement_weight": 0,
    #             "social_weight": 0,
    #             "diversity_weight": 1,
    #             "preference_weight": 0,
    #         },
    #         "students": [
    #             {
    #                 "id": id,
    #                 "relationships": {},
    #                 "attributes": {"1": [1]},
    #             }
    #             for id in above_average_members
    #         ]
    #         + [
    #             {
    #                 "id": id,
    #                 "relationships": {},
    #                 "attributes": {"1": [0]},
    #             }
    #             for id in below_average_members
    #         ],
    #         "team_generation_options": {
    #             "initial_teams": [],
    #             "max_team_size": 3,
    #             "min_team_size": 2,
    #             "total_teams": 0,
    #         },
    #     },
    # )

    team_set = TeamSet.objects.create(course=course, name="Studdy Buddy")

    teams = []
    for course_member_id in above_average_members:
        team = Team.objects.create(
            slug=uuid.uuid4(),
            max_people=10,
            min_people=1,
            team_set=team_set,
        )
        team.members.add(CourseMember.objects.get(id=course_member_id))
        teams.append(team)

    for i, course_member_id in enumerate(below_average_members):
        teams[i % len(teams)].members.add(CourseMember.objects.get(id=course_member_id))

