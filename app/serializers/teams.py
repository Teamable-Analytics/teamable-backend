from rest_framework import serializers

from app.models.teams import Team, TeamSet


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = "__all__"


class TeamSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamSet
        fields = "__all__"
