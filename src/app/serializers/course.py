from rest_framework import serializers

from app.models.course import Course
from app.serializers.organization import OrganizationViewSerializer


class CourseViewSerializer(serializers.ModelSerializer):
    organization = OrganizationViewSerializer(read_only=True)

    class Meta:
        model = Course
        fields = ["id", "name", "organization", "lms_course_id"]


class CourseUpdateSerializer(serializers.ModelSerializer):
    lms_access_token = serializers.CharField(write_only=True)

    class Meta:
        model = Course
        fields = ["name", "organization", "lms_access_token", "lms_course_id"]
