from typing import Tuple, List, Union

from app.canvas.import_attribute import ABOVE_AVERAGE_LABEL, BELOW_AVERAGE_LABEL
from app.models.attribute import Attribute
from app.models.course import Course
import uuid

from app.models.course_member import CourseMember, UserRole
from app.models.team import Team, TeamSet

TEAM_GENERATION_API_URL = "https://api.teamableanalytics.ok.ubc.ca/api/generate/teams/"


def generate_teams(course: Course, attribute: Attribute) -> TeamSet:
    above_average = attribute.options.get(label=ABOVE_AVERAGE_LABEL)
    below_average = attribute.options.get(label=BELOW_AVERAGE_LABEL)

    above_average_members = list(
        above_average.attribute_responses.filter(
            course_member__role=UserRole.STUDENT
        ).values_list("course_member", flat=True)
    )
    below_average_members = list(
        below_average.attribute_responses.filter(
            course_member__role=UserRole.STUDENT
        ).values_list("course_member", flat=True)
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

    num_course_team_sets = course.team_sets.count()
    team_set = TeamSet.objects.create(
        course=course, name=f"Study Buddy - {num_course_team_sets + 1}"
    )

    ordered_students = [*above_average_members, *below_average_members]
    student_pairs: List[Union[Tuple[int, int], Tuple[int, int, int]]] = []

    while len(ordered_students) > 0:
        if len(ordered_students) == 3:
            student_pairs.append(
                (ordered_students[0], ordered_students[1], ordered_students[2])
            )
            break

        first_student = ordered_students.pop(0)
        last_student = ordered_students.pop()
        student_pairs.append((first_student, last_student))

    teams = []
    for student_pair in student_pairs:
        team = Team.objects.create(
            slug=uuid.uuid4(),
            name=f"Team {len(teams) + 1}",
            max_people=10,
            min_people=1,
            team_set=team_set,
        )

        for student in student_pair:
            team.members.add(CourseMember.objects.get(id=student))

        teams.append(team)

    return team_set
