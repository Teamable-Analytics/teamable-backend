from rest_framework import viewsets

from app.models.teams import Team, TeamSet
from app.serializers.teams import TeamSerializer, TeamSetSerializer


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class TeamSetViewSet(viewsets.ModelViewSet):
    queryset = TeamSet.objects.all()
    serializer_class = TeamSetSerializer
