from rest_framework import serializers

from app.models.relationship import Relationship


class RelationshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relationship
        fields = "__all__"
