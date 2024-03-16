from rest_framework import viewsets, permissions

from app.models import TeamTemplate
from app.serializers.team_template import TeamTemplateSerializer


class TeamTemplateViewSet(viewsets.ModelViewSet):
    queryset = TeamTemplate.objects.all()
    serializer_class = TeamTemplateSerializer
    permission_classes = [permissions.IsAuthenticated]
