from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from app.canvas.import_students import import_students_from_canvas
from app.models.course import Course
from app.serializers.course import CourseSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


    @action(detail=True, methods=['post'])
    def import_students_from_lms(self, request, pk=None):
        course = self.get_object()
        import_students_from_canvas(course)
        return Response(status=status.HTTP_200_OK)
