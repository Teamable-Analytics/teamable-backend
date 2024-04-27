from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from django_filters import rest_framework as filters
from app.models.course import Course
from app.serializers.course import CourseSerializer, CustomCourseSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ["id"]

    def get_queryset(self):
        course_id = self.request.query_params.get("id", None)
        if course_id:
            get_object_or_404(Course, pk=course_id)
            return self.queryset
        return self.queryset

    def get_serializer_class(self):
        course_id = self.request.query_params.get("id", None)
        if course_id:
            return CustomCourseSerializer
        return CourseSerializer
