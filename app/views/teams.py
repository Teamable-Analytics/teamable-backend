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
        teamset = self.queryset.filter(teamset=self.kwargs["teamset_id"])
        if not teamset.exists():
            raise Http404
        return teamset


class TeamSetViewSet(viewsets.ModelViewSet):
    queryset = TeamSet.objects.all()
    serializer_class = TeamSetSerializer


class TeamTemplateViewSet(viewsets.ModelViewSet):
    queryset = TeamTemplate.objects.all()
    serializer_class = TeamTemplateSerializer

    def get_queryset(self):
        teamset_template = self.queryset.filter(teamset_template=self.kwargs["teamset_template_id"])
        if not teamset_template.exists():
            raise Http404
        return teamset_template


class TeamSetTemplateViewSet(viewsets.ModelViewSet):
    queryset = TeamSetTemplate.objects.all()
    serializer_class = TeamSetTemplateSerializer
