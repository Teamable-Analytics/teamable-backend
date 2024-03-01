from rest_framework import serializers

from app.models.course_member import CourseMember
from accounts.serializers import UserSerializer
from accounts.serializers import StudentMemberSerializer
from app.serializers.section import SectionSerializer


class CourseMemberSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    sections = SectionSerializer(many=True, read_only=True)

    class Meta:
        model = CourseMember
        fields = "__all__"


class StudentMemberSerializer(serializers.ModelSerializer):
    user = StudentMemberSerializer(read_only=True)
    sections = SectionSerializer(many=True, read_only=True)

    class Meta:
        model = CourseMember
        fields = "__all__"
