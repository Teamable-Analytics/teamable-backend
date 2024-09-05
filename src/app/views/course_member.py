from rest_framework import viewsets

from app.models.course_member import CourseMember, UserRole
from app.paginators.pagination import ExamplePagination
from app.filters.course_member import FilterStudents
from app.serializers.course_member import CourseMemberSerializer

from rest_framework.response import Response


class CourseMemberViewSet(viewsets.GenericViewSet):
    queryset = CourseMember.objects.all()
    serializer_class = CourseMemberSerializer
    pagination_class = ExamplePagination
    ordering_fields = "__all__"
    filter_backends = [FilterStudents]

    def get_students_by_course(self, request, course=None, *args, **kwargs):
        queryset = CourseMember.objects.filter(role=UserRole.STUDENT)
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
