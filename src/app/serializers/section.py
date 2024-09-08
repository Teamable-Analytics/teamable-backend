from rest_framework import serializers

from app.models.section import Section


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ("id", "name")
