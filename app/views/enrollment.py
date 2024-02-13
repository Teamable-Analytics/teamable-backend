from rest_framework import viewsets

from app.models.enrollment import Enrollment
from app.serializers.enrollment import EnrollmentSerializer


class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
