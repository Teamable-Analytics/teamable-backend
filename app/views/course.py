from rest_framework import serializers, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from app.canvas.export_team import export_team_to_canvas
from app.canvas.import_attribute import import_gradebook_attribute_from_canvas
from app.canvas.import_students import import_students_from_canvas
from app.canvas.opt_in_quizz import create_opt_in_quiz_canvas
from app.models.course import Course
from app.models.team import TeamSet
from app.serializers.course import CourseUpdateSerializer, CourseViewSerializer


class ExportTeamSerializer(serializers.ModelSerializer):
    team_set = serializers.PrimaryKeyRelatedField(queryset=TeamSet.objects.all())

    class Meta:
        model = Course
        fields = ["team_set"]

    def validate_team_set(self, value):
        if not value.course == self.instance:
            raise serializers.ValidationError("Team set must belong to the course")
        return value


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseViewSerializer

    def get_serializer_class(self):
        if self.action in ["update", "partial_update"]:
            return CourseUpdateSerializer
        return super().get_serializer_class()

    @action(detail=True, methods=["post"], serializer_class=serializers.Serializer)
    def import_students_from_lms(self, request, pk=None):
        course = self.get_object()
        import_students_from_canvas(course)
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], serializer_class=ExportTeamSerializer)
    def export_team_to_lms(self, request, pk=None):
        serializer = ExportTeamSerializer(instance=self.get_object(), data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Pylance doesn't know that validated_data is valid after is_valid() check
        team_set_id = serializer.validated_data["team_set"]  # type: ignore

        course: Course = self.get_object()
        team_set = course.team_sets.get(pk=team_set_id)

        export_team_to_canvas(team_set)
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], serializer_class=serializers.Serializer)
    def create_opt_in_quiz_lms(self, request, pk=None):
        course = self.get_object()
        create_opt_in_quiz_canvas(course)
        return Response(status=status.HTTP_200_OK)

    # Studdy buddy specific function
    @action(detail=True, methods=["post"], serializer_class=serializers.Serializer)
    def import_gradebook_attribute_from_lms(self, request, pk=None):
        course = self.get_object()
        import_gradebook_attribute_from_canvas(course)
        return Response(status=status.HTTP_200_OK)
