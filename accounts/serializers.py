from rest_framework import serializers
from django.contrib.auth.models import User
from accounts.models import MyUser


class StudentMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ["id", "first_name", "last_name"]


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "first_name", "last_name", "is_staff"]
