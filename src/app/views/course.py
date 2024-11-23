from typing import Type
from rest_framework import serializers, viewsets, status, mixins
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import action
from app.canvas.export_team import export_team_to_canvas
from app.canvas.import_attribute import import_gradebook_attribute_from_canvas
from app.canvas.import_students import import_students_from_canvas
from app.canvas.opt_in_quiz import create_opt_in_quiz_canvas
from app.filters.course_member import FilterStudents
from app.models.attribute import Attribute, AttributeManageType
from app.models.course import Course
from app.models.course_member import UserRole
from app.models.team import TeamSet
from app.paginators.pagination import ExamplePagination
from app.permissions import IsCourseInstructor
from app.serializers.attribute import AttributeSerializer
from app.serializers.course import CourseUpdateSerializer, CourseViewSerializer
from app.serializers.course_member import CourseMemberSerializer
from app.serializers.teams import (
    DisplayManyTeamSetSerializer,
    DisplaySingleTeamSetSerializer,
)
from app.services.team_generation import generate_teams


class ExportTeamSerializer(serializers.ModelSerializer):
    team_set = serializers.PrimaryKeyRelatedField(queryset=TeamSet.objects.all())

    class Meta:
        model = Course
        fields = ["team_set"]

    def validate_team_set(self, value):
        if not value.course == self.instance:
            raise serializers.ValidationError("Team set must belong to the course")
        return value


class CourseTeamSetsSerializer(serializers.ModelSerializer):
    team_sets = DisplayManyTeamSetSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ["team_sets"]


class GenerateTeamsSerializer(serializers.ModelSerializer):
    attribute = serializers.PrimaryKeyRelatedField(queryset=Attribute.objects.all())

    class Meta:
        model = Course
        fields = ["attribute"]

    def validate_attribute(self, value):
        if not value.course == self.instance:
            raise serializers.ValidationError("Attribute must belong to the course")
        return value


class OnboardingProgressSerializer(serializers.ModelSerializer):
    opt_in_quiz_link = serializers.CharField(read_only=True)
    has_created_opt_in_quiz = serializers.BooleanField(read_only=True)
    has_students = serializers.BooleanField(read_only=True)
    has_attribute = serializers.BooleanField(read_only=True)
    has_attribute_responses = serializers.BooleanField(read_only=True)
    has_team_set = serializers.BooleanField(read_only=True)

    class Meta:
        model = Course
        fields = (
            "opt_in_quiz_link",
            "has_created_opt_in_quiz",
            "has_students",
            "has_attribute",
            "has_attribute_responses",
            "has_team_set",
        )


class CourseViewSet(
    mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet
):
    queryset = Course.objects.all()
    serializer_class = CourseViewSerializer
    permission_classes = [IsCourseInstructor]

    def get_serializer_class(
        self,
    ) -> Type[CourseUpdateSerializer | CourseViewSerializer]:
        if self.action in ["update", "partial_update"]:
            return CourseUpdateSerializer
        return CourseViewSerializer

    @action(
        detail=True,
        methods=["post"],
        serializer_class=serializers.Serializer,
        permission_classes=[IsCourseInstructor],
    )
    def import_students_from_lms(self, request, pk=None):
        course = self.get_object()
        import_students_from_canvas(course)
        return Response(status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=["post"],
        serializer_class=ExportTeamSerializer,
        permission_classes=[IsCourseInstructor],
    )
    def export_team_to_lms(self, request, pk=None):
        serializer = ExportTeamSerializer(instance=self.get_object(), data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Pylance doesn't know that validated_data is valid after is_valid() check
        team_set = serializer.validated_data["team_set"]  # type: ignore

        export_team_to_canvas(team_set)
        return Response(status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=["post"],
        serializer_class=serializers.Serializer,
        permission_classes=[IsCourseInstructor],
    )
    def create_opt_in_quiz_lms(self, request, pk=None):
        course = self.get_object()
        create_opt_in_quiz_canvas(course)
        return Response(status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=["get"],
        serializer_class=OnboardingProgressSerializer,
        permission_classes=[IsCourseInstructor],
    )
    def get_onboarding_progress(self, request, pk=None):
        serializer = OnboardingProgressSerializer(
            instance=self.get_object(), data=request.data
        )
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Study buddy specific function
    @action(
        detail=True,
        methods=["post"],
        serializer_class=serializers.Serializer,
        permission_classes=[IsCourseInstructor],
    )
    def import_gradebook_attribute_from_lms(self, request, pk=None):
        course = self.get_object()
        import_gradebook_attribute_from_canvas(course)
        return Response(status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=["post"],
        serializer_class=GenerateTeamsSerializer,
        permission_classes=[IsCourseInstructor],
    )
    def generate_teams(self, request, pk=None):
        course = self.get_object()

        serializer = GenerateTeamsSerializer(instance=course, data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Pylance doesn't know that validated_data is valid after is_valid() check
        attribute = serializer.validated_data["attribute"]  # type: ignore

        team_set = generate_teams(course, attribute)
        return Response({"team_set_id": team_set.pk}, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=["get"],
        serializer_class=CourseTeamSetsSerializer,
        permission_classes=[IsCourseInstructor],
    )
    def get_team_sets(self, request, pk=None):
        team_sets = self.get_object().team_sets.order_by("-updated_at")
        serializer = DisplayManyTeamSetSerializer(instance=team_sets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=["get"],
        serializer_class=serializers.Serializer,
        permission_classes=[IsCourseInstructor],
        url_path=r"team-sets/(?P<team_set_pk>\d+)",
    )
    def get_teams(self, request, pk=None, team_set_pk=None):
        team_set = get_object_or_404(self.get_object().team_sets, pk=team_set_pk)

        serializer = DisplaySingleTeamSetSerializer(
            instance=team_set, data=request.data
        )
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=["get"],
        serializer_class=CourseMemberSerializer,
        pagination_class=ExamplePagination,
        permission_classes=[IsCourseInstructor],
        url_path="students",
    )
    def get_students_by_course(self, request, pk=None):
        queryset = self.get_object().course_members.filter(role=UserRole.STUDENT)
        queryset = FilterStudents().filter_queryset(self.request, queryset, self)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

    @action(
        detail=True,
        methods=["get"],
        permission_classes=[IsCourseInstructor],
        url_path="grade-attributes",
    )
    def get_grade_attributes(self, request, pk=None):
        course: Course = self.get_object()
        grade_attributes = course.attributes.filter(
            manage_type=AttributeManageType.GRADE
        )
        return Response(
            AttributeSerializer(grade_attributes, many=True).data,
            status=status.HTTP_200_OK,
        )
