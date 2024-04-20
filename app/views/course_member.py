from rest_framework import viewsets

from app.models.course_member import CourseMember, UserRole
from app.paginators.pagination import ExamplePagination
from app.models.section import Section
from app.filters.course_member import FilterStudents
from app.serializers.course_member import (
    CourseMemberSerializer,
    UpdateStudentSectionsRequest,
)

from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

from django.db import transaction


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
    @transaction.atomic
    def update_sections(self, request, *args, **kwargs):
        course_member = self.get_object()

        if course_member.role != UserRole.STUDENT:
            return Response(
                {"message": "Only students can be assigned to sections."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        request_body_serializer = UpdateStudentSectionsRequest(
            instance=course_member,
            data=request.data,
            context={"course": course_member.course},
        )
        if request_body_serializer.is_valid(raise_exception=True):
            section_ids = request_body_serializer._validated_data.get("sections")
            print(section_ids)
            proposed_sections_update = Section.objects.filter(
                id__in=section_ids, course=course_member.course
            )
            course_member.sections.set(proposed_sections_update)
            course_member.save()

        response_course_member_serializer = self.get_serializer(course_member)
        return Response(response_course_member_serializer.data)
