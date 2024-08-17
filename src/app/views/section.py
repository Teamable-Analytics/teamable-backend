from rest_framework import viewsets

from app.models.section import Section
from app.serializers.section import SectionSerializer


class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
