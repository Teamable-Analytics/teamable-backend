from rest_framework import viewsets

from app.models.course_member import CourseMember
from app.serializers.course_member import StudentMemberSerializer
from app.paginators.pagination import ExamplePagination
from app.filters.course_member import FilterStudents


class CourseMemberViewSet(viewsets.ModelViewSet):
    queryset = CourseMember.objects.all()
    serializer_class = StudentMemberSerializer
    pagination_class = ExamplePagination
    ordering_fields = "__all__"
    filter_backends = [FilterStudents]
