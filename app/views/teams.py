from rest_framework import viewsets

from app.models import Team, TeamSet, TeamSetTemplate, TeamTemplate
from app.serializers.teams import (
    TeamSerializer,
    TeamSetSerializer,
    TeamTemplateSerializer,
    TeamSetTemplateSerializer,
    OutlinedTeamSetTemplateSerializer,
)


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class TeamSetViewSet(viewsets.ModelViewSet):
    queryset = TeamSet.objects.all()
    serializer_class = TeamSetSerializer


class TeamTemplateViewSet(viewsets.ModelViewSet):
    queryset = TeamTemplate.objects.all()
    serializer_class = TeamTemplateSerializer


class TeamSetTemplateViewSet(viewsets.ModelViewSet):
    queryset = TeamSetTemplate.objects.all()
    serializer_class = TeamSetTemplateSerializer


class OutlinedTeamSetTemplateViewSet(viewsets.ModelViewSet):
    queryset = TeamSetTemplate.objects.all()
    serializer_class = OutlinedTeamSetTemplateSerializer
