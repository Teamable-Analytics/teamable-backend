from rest_framework import serializers
from app.models import TeamTemplate, Team, TeamSetTemplate, TeamTemplateRequirement, TeamRequirement


class TeamSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamSetTemplate
        fields = '__all__'


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'


class TeamRequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamRequirement
        fields = '__all__'


class TeamSetTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamSetTemplate
        fields = '__all__'


class TeamTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamTemplate
        fields = '__all__'


class TeamTemplateRequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamTemplateRequirement
        fields = '__all__'
