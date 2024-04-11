from rest_framework import viewsets

from app.models.course_member import CourseMember
from app.paginators.pagination import ExamplePagination
from app.models.section import Section
from app.models.course import Course
from app.filters.course_member import FilterStudents
from app.serializers.course_member import CourseMemberSerializer
from app.serializers.section import SectionSerializer

from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

from django.shortcuts import get_object_or_404


class CourseMemberViewSet(viewsets.ModelViewSet):
    queryset = CourseMember.objects.all()
    serializer_class = CourseMemberSerializer
    pagination_class = ExamplePagination
    ordering_fields = "__all__"
    filter_backends = [FilterStudents]

    def get_students_by_course(self, request, course=None, *args, **kwargs):
        queryset = CourseMember.objects.all()
        if course is not None:
            queryset = queryset.filter(course=course)

        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

    @action(detail=True, methods=["put"], url_path="update-sections")
    def update_sections(self, request, *args, **kwargs):
        course_member = self.get_object()

        section_ids = request.data.get("sections")

        if course_member.role != CourseMember.STUDENT:
            return Response(
                {"message": "Only students can be assigned to sections."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if section_ids is None:
            return Response(
                {"message": "Sections are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not isinstance(section_ids, list):
            return Response(
                {"message": "Sections must be a list."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            section_ids = [int(section_id) for section_id in section_ids]
        except ValueError:
            return Response(
                {"message": "Sections must be integers."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        attempted_sections_returned = Section.objects.filter(id__in=section_ids)
        if len(attempted_sections_returned) != len(section_ids):
            return Response(
                {"message": "One or more sections do not exist."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        proposed_sections_update = Section.objects.filter(id__in=section_ids)
        course_member.sections.set(proposed_sections_update)
        serializer = self.get_serializer(course_member)
        return Response(serializer.data)
