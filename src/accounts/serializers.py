from django.contrib.auth.models import User
from accounts.models import MyUser
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from app.models.course_member import CourseMember, CourseMemberTokenError
from app.serializers.course_member import CourseMemberListSerializer
import accounts.error_messages as ERROR_MESSAGES
from django.contrib.auth import authenticate

class StudentMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ["id", "first_name", "last_name"]


class MyUserSerializer(serializers.ModelSerializer):
    course_memberships = CourseMemberListSerializer(read_only=True, many=True)

    class Meta:
        model = MyUser
        fields = ["id", "username", "first_name", "last_name", "email", "is_staff", "course_memberships"]


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
                message=ERROR_MESSAGES.EMAIL.UNIQUE,
            )
        ],
        error_messages=ERROR_MESSAGES.EMAIL.ERROR_MESSAGES,
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"},
        validators=[validate_password],
        error_messages=ERROR_MESSAGES.PASSWORD.ERROR_MESSAGES,
    )

    token = serializers.CharField(write_only=True)

    class Meta:
        model = MyUser
        fields = ("email", "password", "token")

    def validate(self, data):
        token = data.get("token")

        try:
            course_member = CourseMember.validate_token(token)
            data["course_member"] = course_member
        except CourseMemberTokenError:
            raise serializers.ValidationError(ERROR_MESSAGES.SIGNUP.INVALID_TOKEN)
        return data

    def create(self, validated_data):
        user = MyUser.objects.create_user(
            username=validated_data["email"],
            email=validated_data["email"],
            is_active=True,
        )

        # assign couse_member to user
        course_member = validated_data["course_member"]
        course_member.set_user(user)

        user.set_password(validated_data["password"])
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(
        required=True,
        write_only=True,
        error_messages=ERROR_MESSAGES.EMAIL.ERROR_MESSAGES,
    )
    password = serializers.CharField(
        required=True,
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
        error_messages=ERROR_MESSAGES.PASSWORD.ERROR_MESSAGES,
    )
    token = serializers.CharField(read_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        user = authenticate(
            request=self.context.get("request"), username=email, password=password
        )

        # The authenticate call simply returns None for is_active=False
        # users. (Assuming the default ModelBackend authentication
        # backend.)
        if not user:
            raise serializers.ValidationError(
                ERROR_MESSAGES.PASSWORD.INVALID, code="authorization"
            )

        data["user"] = user
        return data
