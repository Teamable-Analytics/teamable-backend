from rest_framework import viewsets

from app.models.projects import Project, ProjectSet
from app.serializers.projects import ProjectSerializer, ProjectSetSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProjectSetViewSet(viewsets.ModelViewSet):
    queryset = ProjectSet.objects.all()
    serializer_class = ProjectSetSerializer
