from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from app.models.section import Section
from app.models.course import Course
from app.serializers.section import SectionSerializer


class CourseSectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer

    def get_course_sections(self, request, course):
        if not Course.objects.filter(id=course).exists():
            return Response({"error": "Course not found"}, status=404)
        sections = Section.objects.filter(course=course)
        serializer = SectionSerializer(sections, many=True)
        return Response(serializer.data)
