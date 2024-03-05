from rest_framework import viewsets

from app.models.course_member import CourseMember
from app.paginators.pagination import ExamplePagination
from app.filters.course_member import FilterStudents
from app.serializers.course_member import CourseMemberSerializer


class CourseMemberViewSet(viewsets.ModelViewSet):
    queryset = CourseMember.objects.all()
    serializer_class = CourseMemberSerializer
    pagination_class = ExamplePagination
    ordering_fields = "__all__"
    filter_backends = [FilterStudents]
