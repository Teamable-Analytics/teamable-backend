from rest_framework import viewsets, permissions

from app.models import TeamTemplate, Team, TeamSetTemplate, TeamRequirement, TeamSet, TeamTemplateRequirement
from app.serializers.team import (
    TeamTemplateSerializer,
    TeamSerializer,
    TeamSetSerializer,
    TeamRequirementSerializer,
    TeamSetTemplateSerializer,
    TeamTemplateRequirementSerializer
)


class TeamSetViewSet(viewsets.ModelViewSet):
    queryset = TeamSet.objects.all()
    serializer_class = TeamSetSerializer
    permission_classes = [permissions.IsAuthenticated]


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticated]


class TeamRequirementViewSet(viewsets.ModelViewSet):
    queryset = TeamRequirement.objects.all()
    serializer_class = TeamRequirementSerializer
    permission_classes = [permissions.IsAuthenticated]


class TeamSetTemplateViewSet(viewsets.ModelViewSet):
    queryset = TeamSetTemplate.objects.all()
    serializer_class = TeamSetTemplateSerializer
    permission_classes = [permissions.IsAuthenticated]


class TeamTemplateViewSet(viewsets.ModelViewSet):
    queryset = TeamTemplate.objects.all()
    serializer_class = TeamTemplateSerializer
    permission_classes = [permissions.IsAuthenticated]


class TeamTemplateRequirementViewSet(viewsets.ModelViewSet):
    queryset = TeamTemplateRequirement.objects.all()
    serializer_class = TeamTemplateRequirementSerializer
    permission_classes = [permissions.IsAuthenticated]
