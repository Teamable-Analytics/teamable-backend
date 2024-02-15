from rest_framework import serializers

from app.models.course_member import CourseMember


class CourseMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseMember
        fields = "__all__"
