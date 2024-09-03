from rest_framework import serializers

from app.models import Organization


class OrganizationViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ("name", "lms_type")
