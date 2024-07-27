from rest_framework import serializers
from django.contrib.auth.models import User
from accounts.models import MyUser
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from app.models.course_member import CourseMember


class StudentMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ["id", "first_name", "last_name"]


class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ["id", "username", "first_name", "last_name", "email", "is_staff"]


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "is_staff"]


class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(
                queryset=MyUser.objects.all(),
            )
        ],
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"},
        validators=[validate_password],
    )

    token = serializers.CharField(write_only=True)

    class Meta:
        model = MyUser
        fields = ("email", "password", "token")

    def create(self, validated_data):
        user = MyUser.objects.create_user(
            username=validated_data["email"],
            email=validated_data["email"],
            is_active=True,
        )

        # assign couse_member to user
        CourseMember.set_user_by_token(user, validated_data["token"])

        user.set_password(validated_data["password"])
        user.save()
        return user
