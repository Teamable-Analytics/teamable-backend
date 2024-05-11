from django.http import Http404
from rest_framework import viewsets
from django.shortcuts import get_object_or_404

from app.models import Team, TeamSet, TeamSetTemplate, TeamTemplate
from app.serializers.teams import (
    TeamSerializer,
    TeamSetSerializer,
    TeamTemplateSerializer,
    TeamSetTemplateSerializer,
)


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    def get_queryset(self):
        # Check if teamset exists
        get_object_or_404(TeamSet, pk=self.kwargs["teamset_id"])
        # Return the team that belongs to the teamset
        return self.queryset.filter(team_set=self.kwargs["teamset_id"])


class TeamSetViewSet(viewsets.ModelViewSet):
    queryset = TeamSet.objects.all()
    serializer_class = TeamSetSerializer


class TeamTemplateViewSet(viewsets.ModelViewSet):
    queryset = TeamTemplate.objects.all()
    serializer_class = TeamTemplateSerializer

    def get_queryset(self):
        # Check if teamset_template_id exists
        get_object_or_404(TeamSetTemplate, pk=self.kwargs["teamset_template_id"])
        # Return the team_template that belongs to the teamset_template
        return self.queryset.filter(team_set=self.kwargs["teamset_template_id"])


class TeamSetTemplateViewSet(viewsets.ModelViewSet):
    queryset = TeamSetTemplate.objects.all()
    serializer_class = TeamSetTemplateSerializer
