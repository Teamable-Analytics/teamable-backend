from rest_framework import serializers
from accounts.models import MyUser
from app.models.section import Section
from app.models.course_member import CourseMember


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = "__all__"


class StudentMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ["id", "first_name", "last_name"]
