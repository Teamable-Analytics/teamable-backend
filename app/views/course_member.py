from rest_framework import viewsets

from app.models.course_member import CourseMember
from app.serializers.course_member import CourseMemberSerializer


class CourseMemberViewSet(viewsets.ModelViewSet):
    queryset = CourseMember.objects.all()
    serializer_class = CourseMemberSerializer
