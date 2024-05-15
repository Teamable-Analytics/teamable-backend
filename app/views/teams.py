from rest_framework import viewsets
from django.shortcuts import get_object_or_404, get_list_or_404

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
        get_object_or_404(TeamSet, pk=self.kwargs["teamset_id"])
        return get_list_or_404(self.queryset, team_set_id=self.kwargs["teamset_id"])


class TeamSetViewSet(viewsets.ModelViewSet):
    queryset = TeamSet.objects.all()
    serializer_class = TeamSetSerializer


class TeamTemplateViewSet(viewsets.ModelViewSet):
    queryset = TeamTemplate.objects.all()
    serializer_class = TeamTemplateSerializer

    def get_queryset(self):
        teamset_template = get_object_or_404(TeamSetTemplate, pk=self.kwargs["teamset_template_id"])
        return get_list_or_404(self.queryset, team_set_id=teamset_template.pk)


class TeamSetTemplateViewSet(viewsets.ModelViewSet):
    queryset = TeamSetTemplate.objects.all()
    serializer_class = TeamSetTemplateSerializer
