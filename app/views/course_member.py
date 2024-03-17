from rest_framework import viewsets

from app.models.course_member import CourseMember
from app.paginators.pagination import ExamplePagination
from app.filters.course_member import FilterStudents
from app.serializers.course_member import CourseMemberSerializer


from rest_framework.decorators import action


class CourseMemberViewSet(viewsets.ModelViewSet):
    queryset = CourseMember.objects.all()
    serializer_class = CourseMemberSerializer

    @action(detail=False, methods=["get"], url_path="course/(?P<course>[^/.]+)")
    def by_course(self, request, course):
        queryset = CourseMember.objects.filter(course=course)
        serializer = self.get_serializer(queryset, many=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

    pagination_class = ExamplePagination
    ordering_fields = "__all__"
    filter_backends = [FilterStudents]
