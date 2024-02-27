from rest_framework import serializers

from app.models.course import Course


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"

    def __str__(self):
        return self.name
