from rest_framework import serializers

from app.models.course import Course
from app.serializers.attribute import AttributeSerializer


class CourseSerializer(serializers.ModelSerializer):
    attributes = AttributeSerializer(many=True, read_only=True)
    
    class Meta:
        model = Course
        fields = "__all__"
