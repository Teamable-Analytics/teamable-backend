from rest_framework import serializers

from app.models.course import Course
from app.serializers.attribute import AttributeSerializer


class CourseViewSerializer(serializers.ModelSerializer):
    attributes = AttributeSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ["id", "name", "organization", "lms_course_id", "attributes"]


class CourseUpdateSerializer(serializers.ModelSerializer):
    lms_access_token = serializers.CharField(write_only=True)

    class Meta:
        model = Course
        fields = ["name", "organization", "lms_access_token", "lms_course_id"]
