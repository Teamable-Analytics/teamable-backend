from rest_framework import serializers
from app.models import TeamTemplate


class TeamTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamTemplate
        fields = '__all__'
