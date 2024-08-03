from rest_framework import viewsets

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


class TeamSetViewSet(viewsets.ModelViewSet):
    queryset = TeamSet.objects.all()
    serializer_class = TeamSetSerializer


class TeamTemplateViewSet(viewsets.ModelViewSet):
    queryset = TeamTemplate.objects.all()
    serializer_class = TeamTemplateSerializer


class TeamSetTemplateViewSet(viewsets.ModelViewSet):
    queryset = TeamSetTemplate.objects.all()
    serializer_class = TeamSetTemplateSerializer

    def get_queryset(self):
        queryset = TeamSetTemplate.objects.all()
        is_detailed = self.request.query_params.get("detailed", None)
        if is_detailed is not None and is_detailed.lower() == "true":
            return queryset
        return queryset.values("name", "id")
