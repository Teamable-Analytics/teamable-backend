from rest_framework import serializers

from app.models.course_member import CourseMember
from app.serializers.section import SectionSerializer


class CourseMemberSerializer(serializers.ModelSerializer):
    sections = SectionSerializer(many=True, read_only=True)
    lms_link = serializers.CharField(read_only=True)

    class Meta:
        model = CourseMember
        fields = (
            "id",
            "lms_id",
            "sis_user_id",
            "name",
            "first_name",
            "last_name",
            "role",
            "lms_link",
            "sections",
        )


class DisplayCourseMemberSerializer(serializers.ModelSerializer):
    lms_link = serializers.CharField(read_only=True)

    class Meta:
        model = CourseMember
        fields = (
            "id",
            "lms_id",
            "sis_user_id",
            "name",
            "first_name",
            "last_name",
            "role",
            "lms_link",
        )


class CourseMemberListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseMember
        fields = ("course",)
