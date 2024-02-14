from rest_framework import serializers

from app.models.projects import ProjectSet, Project


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"


class ProjectSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectSet
        fields = "__all__"
