from rest_framework import serializers

from app.models import (
    Team,
    TeamSet,
    TeamTemplate,
    TeamSetTemplate,
    TeamRequirement,
    TeamTemplateRequirement,
)
from app.serializers.attribute import AttributeSerializer
from app.serializers.course_member import (
    CourseMemberSerializer,
    DisplayCourseMemberSerializer,
)


class TeamRequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamRequirement
        fields = "__all__"


class TeamSerializer(serializers.ModelSerializer):
    members = CourseMemberSerializer(many=True, read_only=True)
    requirements = TeamRequirementSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = "__all__"


class DisplaySingleTeamSerializer(serializers.ModelSerializer):
    members = DisplayCourseMemberSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = ("id", "slug", "name", "members")


class TeamSetSerializer(serializers.ModelSerializer):
    teams = TeamSerializer(many=True, read_only=True)

    class Meta:
        model = TeamSet
        fields = "__all__"


class DisplaySingleTeamSetSerializer(serializers.ModelSerializer):
    teams = DisplaySingleTeamSerializer(many=True, read_only=True)
    name = serializers.CharField(read_only=True)
    unassigned_students = CourseMemberSerializer(many=True, read_only=True)

    class Meta:
        model = TeamSet
        fields = ("id", "name", "teams", "unassigned_students")


class DisplayManyTeamSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamSet
        fields = ("id", "name")


class TeamTemplateRequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamTemplateRequirement
        fields = "__all__"


class TeamTemplateSerializer(serializers.ModelSerializer):
    requirements = TeamTemplateRequirementSerializer(many=True, read_only=True)

    class Meta:
        model = TeamTemplate
        fields = "__all__"


class TeamSetTemplateSerializer(serializers.ModelSerializer):
    teams = TeamTemplateSerializer(many=True, read_only=True)
    attributes = AttributeSerializer(many=True, read_only=True)

    class Meta:
        model = TeamSetTemplate
        fields = "__all__"
