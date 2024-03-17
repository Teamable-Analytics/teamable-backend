from rest_framework import viewsets

from app.models.course_member import CourseMember
from app.paginators.pagination import ExamplePagination
from app.filters.course_member import FilterStudents
from app.serializers.course_member import CourseMemberSerializer


from rest_framework.decorators import action
from rest_framework.response import Response


class CourseMemberViewSet(viewsets.ModelViewSet):
    queryset = CourseMember.objects.all()
    serializer_class = CourseMemberSerializer
    pagination_class = ExamplePagination
    ordering_fields = "__all__"
    filter_backends = [FilterStudents]

    @action(detail=False, methods=["get"], url_path="course/(?P<course>[^/.]+)")
    def by_course(self, request, course):
        queryset = CourseMember.objects.filter(course=course)

        for backend in self.filter_backends:
            queryset = backend().filter_queryset(request, queryset, self)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
