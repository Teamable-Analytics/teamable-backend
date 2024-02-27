from rest_framework import viewsets

from app.models.course_member import CourseMember
from app.serializers.course_member import CourseMemberSerializer
from app.models.pagination import StandardResultsSetPagination
from app.filters.course_member import FilterStudents

class CourseMemberViewSet(viewsets.ModelViewSet):
    queryset = CourseMember.objects.all()
    serializer_class = CourseMemberSerializer
    pagination_class = StandardResultsSetPagination
    ordering_fields = "__all__"
    filter_backends = [FilterStudents]