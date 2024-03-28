from rest_framework import viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from app.models.section import Section
from app.models.course import Course
from app.serializers.section import SectionSerializer


class CourseSectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer

    def get_course_sections(self, request, course):
        course = get_object_or_404(Course, pk=course)
        course.sections.set(Section.objects.filter(course=course))
        serializer = SectionSerializer(course.sections, many=True)
        return Response(serializer.data)
