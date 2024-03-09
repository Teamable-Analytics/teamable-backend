from rest_framework import filters
from app.models.attribute import Attribute

from app.models.course_member import CourseMember, UserRole


class FilterAttributes(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if request.GET.get("course_id", None):
            return queryset

        course_member = CourseMember.objects.get(user=request.user)
        if request.user.is_staff:
            pass
        elif (
            course_member.role == UserRole.STUDENT
            or course_member.role == UserRole.INSTRUCTOR
        ):
            queryset = queryset.filter(course_id=course_member.course.id)
        else:
            queryset = Attribute.objects.none()

        return queryset
